import platform
import psutil
import datetime
import json
import paramiko
from backend.collectors.base import BaseCollector
from backend.models.host import Host
from backend.models.inventory import Inventory
from backend.config.settings import settings

class InventoryCollector(BaseCollector):
    name = "InventoryCollector"

    def _get_local_inventory(self) -> dict:
        """Gathers hardware and OS specifications of the local machine"""
        try:
            nics = []
            for name, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket_address_family_ipv4():
                        nics.append({"interface": name, "ip": addr.address})

            return {
                "os": {
                    "system": platform.system(),
                    "release": platform.release(),
                    "version": platform.version(),
                    "machine": platform.machine(),
                    "node": platform.node()
                },
                "cpu": {
                    "processor": platform.processor(),
                    "cores_physical": psutil.cpu_count(logical=False),
                    "cores_logical": psutil.cpu_count(logical=True),
                    "freq_max_mhz": psutil.cpu_freq().max if psutil.cpu_freq() else 0
                },
                "memory": {
                    "total_gb": round(psutil.virtual_memory().total / (1024**3), 2)
                },
                "disk": {
                    "total_gb": round(psutil.disk_usage('/').total / (1024**3), 2)
                },
                "network": nics
            }
        except Exception as e:
            # Simple fallback
            return {
                "os": {"system": platform.system(), "release": platform.release()},
                "cpu": {"cores": psutil.cpu_count()},
                "memory": {"total_gb": round(psutil.virtual_memory().total / (1024**3), 2)},
                "disk": {"total_gb": round(psutil.disk_usage('/').total / (1024**3), 2)}
            }

    def _get_ssh_inventory(self, ip: str, port: int) -> dict:
        """Attempts to execute basic probe commands over SSH for inventory data"""
        if not settings.SSH_USER:
            return {"status": "unauthorized", "details": "No credentials supplied"}
            
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        
        try:
            if settings.SSH_KEY_PATH:
                client.connect(ip, port=port, username=settings.SSH_USER, key_filename=settings.SSH_KEY_PATH, timeout=5)
            else:
                client.connect(ip, port=port, username=settings.SSH_USER, password=settings.SSH_PASSWORD, timeout=5)
                
            inventory_data = {}
            
            # Read OS
            _, stdout, _ = client.exec_command("uname -a")
            inventory_data["os_kernel"] = stdout.read().decode('utf-8').strip()
            
            # Read CPU
            _, stdout, _ = client.exec_command("nproc")
            inventory_data["cpu_cores"] = stdout.read().decode('utf-8').strip()
            
            # Read RAM
            _, stdout, _ = client.exec_command("free -m")
            free_output = stdout.read().decode('utf-8')
            for line in free_output.splitlines():
                if "Mem:" in line:
                    parts = line.split()
                    inventory_data["ram_total_mb"] = parts[1]
            
            # Read Disk
            _, stdout, _ = client.exec_command("df -h / | tail -n 1")
            disk_line = stdout.read().decode('utf-8').split()
            if len(disk_line) >= 2:
                inventory_data["disk_total_size"] = disk_line[1]
                inventory_data["disk_used_percent"] = disk_line[4]

            client.close()
            return {"status": "success", "specs": inventory_data}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def run(self):
        if not self.is_enabled():
            return

        hosts = self.db.query(Host).all()
        for host in hosts:
            specs = {}
            if host.ip == "127.0.0.1":
                specs = self._get_local_inventory()
                host.os = f"{specs.get('os', {}).get('system', 'Linux')} ({specs.get('os', {}).get('release', '')})"
            elif host.ip == settings.SSH_HOST and settings.SSH_USER:
                # Target supports SSH configuration probe
                ssh_res = self._get_ssh_inventory(host.ip, settings.SSH_PORT)
                if ssh_res.get("status") == "success":
                    specs = ssh_res["specs"]
                    host.os = specs.get("os_kernel", "Linux (SSH Verified)")
                else:
                    specs = {"error": ssh_res.get("message")}
            else:
                # External Cloudflare host or unsupported ssh
                specs = {
                    "probe_status": "passive",
                    "details": "External monitoring target. Local scan details restricted to port audit and HTTP/HTTPS metadata."
                }
                
            # Write/Update inventory items
            for comp_type, data in specs.items():
                if comp_type in ["os", "cpu", "memory", "disk", "network", "specs", "probe_status"]:
                    inv_item = self.db.query(Inventory).filter(
                        Inventory.host_id == host.id,
                        Inventory.component_type == comp_type
                    ).first()
                    
                    if not inv_item:
                        inv_item = Inventory(
                            host_id=host.id,
                            component_type=comp_type
                        )
                        self.db.add(inv_item)
                        
                    inv_item.details = json.dumps(data)
                    inv_item.updated_at = datetime.datetime.utcnow()
                    
            self.log_message(host.id, host.ip, f"Inventory specifications updated.", "Info", "Inventory")
            self.db.commit()

def socket_address_family_ipv4():
    import socket
    return socket.AF_INET

if __name__ == "__main__":
    collector = InventoryCollector()
    try:
        collector.run()
    finally:
        collector.close()
