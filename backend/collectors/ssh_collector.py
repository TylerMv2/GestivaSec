import socket
import datetime
import paramiko
import json
from backend.collectors.base import BaseCollector
from backend.models.service import Service
from backend.config.settings import settings

class SSHCollector(BaseCollector):
    name = "SSHCollector"

    def _get_ssh_banner(self, ip: str, port: int) -> str:
        """Reads SSH banner without authenticating"""
        try:
            with socket.create_connection((ip, port), timeout=3) as sock:
                banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
                return banner
        except Exception:
            return ""

    def _test_ssh_login(self, ip: str, port: int) -> tuple[bool, str]:
        """Attempts SSH authentication with credentials from settings (if configured)"""
        if not settings.SSH_USER:
            return True, "Authentication credentials not configured. Port is open."
        
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            if settings.SSH_KEY_PATH:
                client.connect(
                    hostname=ip,
                    port=port,
                    username=settings.SSH_USER,
                    key_filename=settings.SSH_KEY_PATH,
                    timeout=5,
                    banner_timeout=5
                )
            else:
                client.connect(
                    hostname=ip,
                    port=port,
                    username=settings.SSH_USER,
                    password=settings.SSH_PASSWORD,
                    timeout=5,
                    banner_timeout=5
                )
            client.close()
            return True, "Authentication Succeeded"
        except paramiko.AuthenticationException:
            return False, "Authentication Failed"
        except Exception as e:
            return False, f"Connection Failed: {e}"

    def run(self):
        if not self.is_enabled():
            return

        ssh_services = self.db.query(Service).filter(Service.name == "SSH").all()
        for service in ssh_services:
            host = service.host
            banner = self._get_ssh_banner(host.ip, service.port)
            
            service.last_check = datetime.datetime.utcnow()
            meta = json.loads(service.metadata_json or "{}")
            
            if banner:
                service.status = "UP"
                service.version = banner
                meta["banner"] = banner
                
                # Check login if it's the authorized ssh target
                if host.ip == settings.SSH_HOST:
                    login_ok, login_msg = self._test_ssh_login(host.ip, service.port)
                    meta["login_status"] = login_msg
                    
                    if not login_ok and "Authentication Failed" in login_msg:
                        self.raise_alert(
                            host_id=host.id,
                            level="Important",
                            source=f"SSH_Auth_{service.id}",
                            description=f"SSH Authentication failed for user '{settings.SSH_USER}' on host {host.hostname} ({host.ip})."
                        )
                        self.log_message(host.id, host.ip, f"SSH Login failed: {login_msg}", "Error", "SSH")
                    else:
                        self.resolve_alerts(host.id, f"SSH_Auth_{service.id}")
                        self.log_message(host.id, host.ip, f"SSH Port 22 check: {login_msg}", "Info", "SSH")
                else:
                    self.log_message(host.id, host.ip, f"SSH service detected: {banner}", "Info", "SSH")
                
                self.resolve_alerts(host.id, f"SSH_{service.id}")
            else:
                service.status = "DOWN"
                service.response_time_ms = 0.0
                self.raise_alert(
                    host_id=host.id,
                    level="Critical",
                    source=f"SSH_{service.id}",
                    description=f"SSH service on port {service.port} of {host.hostname} is unresponsive."
                )
                self.log_message(host.id, host.ip, f"SSH service on port {service.port} is down.", "Error", "SSH")
            
            service.metadata_json = json.dumps(meta)
            self.db.commit()

if __name__ == "__main__":
    collector = SSHCollector()
    try:
        collector.run()
    finally:
        collector.close()
