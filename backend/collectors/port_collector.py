import socket
import json
import datetime
from backend.collectors.base import BaseCollector
from backend.models.host import Host
from backend.models.service import Service

class PortCollector(BaseCollector):
    name = "PortCollector"

    def _scan_port(self, ip: str, port: int) -> bool:
        """Attempts socket connection to check if port is open"""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1.5)
                res = s.connect_ex((ip, port))
                return res == 0
        except Exception:
            return False

    def run(self):
        if not self.is_enabled():
            return

        # Scan ports for all hosts
        hosts = self.db.query(Host).all()
        for host in hosts:
            try:
                authorized_ports = json.loads(host.ports_authorized or "[]")
            except Exception:
                authorized_ports = []
                
            # Scan authorized ports + standard administration/recon ports
            # Standard scan set to audit unexpected exposures
            standard_ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 1433, 3306, 3389, 8000, 8080]
            scan_set = sorted(list(set(authorized_ports + standard_ports)))
            
            open_ports = []
            for port in scan_set:
                is_open = self._scan_port(host.ip, port)
                if is_open:
                    open_ports.append(port)
                    
                    # Update/create service entry if this is a standard service
                    svc_name = {
                        21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 
                        53: "DNS", 80: "HTTP", 443: "HTTPS", 445: "SMB", 
                        1433: "MSSQL", 3306: "MySQL", 3389: "RDP", 
                        8000: "HTTP (API)", 8080: "HTTP (Alt)"
                    }.get(port, f"Service_{port}")
                    
                    svc = self.db.query(Service).filter(
                        Service.host_id == host.id,
                        Service.port == port
                    ).first()
                    
                    if not svc:
                        # Auto-discover service
                        svc = Service(
                            host_id=host.id,
                            name=svc_name,
                            port=port,
                            status="UP",
                            last_check=datetime.datetime.utcnow()
                        )
                        self.db.add(svc)
                    else:
                        svc.status = "UP"
                        svc.last_check = datetime.datetime.utcnow()
                else:
                    # Update existing service to DOWN if it's closed
                    svc = self.db.query(Service).filter(
                        Service.host_id == host.id,
                        Service.port == port
                    ).first()
                    if svc:
                        svc.status = "DOWN"
                        svc.last_check = datetime.datetime.utcnow()
            
            # Check for unauthorized open ports
            unauthorized_open = [p for p in open_ports if p not in authorized_ports]
            alert_source = f"PortAudit_{host.id}"
            
            if unauthorized_open:
                self.raise_alert(
                    host_id=host.id,
                    level="Important",
                    source=alert_source,
                    description=f"Security Audit: Unauthorized open ports detected on host {host.hostname} ({host.ip}): {unauthorized_open}"
                )
                self.log_message(host.id, host.ip, f"Unauthorized open ports found: {unauthorized_open}", "Warn", "PortAudit")
            else:
                self.resolve_alerts(host.id, alert_source)
                self.log_message(host.id, host.ip, f"Port scan completed. Open ports: {open_ports}", "Info", "PortAudit")
                
            self.db.commit()

if __name__ == "__main__":
    collector = PortCollector()
    try:
        collector.run()
    finally:
        collector.close()
