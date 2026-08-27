import time
import requests
import datetime
import json
from backend.collectors.base import BaseCollector
from backend.models.service import Service

class HTTPSCollector(BaseCollector):
    name = "HTTPSCollector"

    def _check_https(self, ip: str, port: int, hostname: str) -> tuple[bool, float, int, str]:
        """
        Performs an HTTPS check.
        """
        url = f"https://{hostname}:{port}/" if hostname else f"https://{ip}:{port}/"
        start = time.time()
        try:
            res = requests.get(url, timeout=5, headers={"User-Agent": "GestivaObservability/1.0"}, verify=True)
            latency = (time.time() - start) * 1000
            server = res.headers.get("Server", "Unknown")
            return True, latency, res.status_code, server
        except requests.exceptions.SSLError as ssl_err:
            return False, 0.0, 495, f"SSL Handshake Error: {ssl_err}"
        except Exception as e:
            return False, 0.0, 0, str(e)

    def run(self):
        if not self.is_enabled():
            return

        # Query HTTPS services
        https_services = self.db.query(Service).filter(Service.name == "HTTPS").all()
        
        for service in https_services:
            host = service.host
            success, latency, status_code, server = self._check_https(host.ip, service.port, host.hostname)
            
            service.last_check = datetime.datetime.utcnow()
            meta = json.loads(service.metadata_json or "{}")
            meta["status_code"] = status_code
            meta["details"] = server
            service.metadata_json = json.dumps(meta)
            
            if success and status_code < 500:
                service.status = "UP"
                service.response_time_ms = latency
                if server != "Unknown" and not server.startswith("SSL Handshake"):
                    service.version = server
                self.resolve_alerts(host.id, f"HTTPS_{service.id}")
                self.log_message(host.id, host.ip, f"HTTPS check on port {service.port} succeeded (Status: {status_code}) in {latency:.2f}ms", "Info", "HTTPS")
            else:
                service.status = "DOWN"
                service.response_time_ms = 0.0
                level = "Critical"
                if status_code == 495:
                    level = "Important"  # SSL error is critical but specifically security-related
                
                self.raise_alert(
                    host_id=host.id,
                    level=level,
                    source=f"HTTPS_{service.id}",
                    description=f"HTTPS service on port {service.port} failed. Code: {status_code}. Details: {server}"
                )
                self.log_message(host.id, host.ip, f"HTTPS check on port {service.port} failed. Code: {status_code}. Error: {server}", "Error", "HTTPS")
            
            self.db.commit()

if __name__ == "__main__":
    collector = HTTPSCollector()
    try:
        collector.run()
    finally:
        collector.close()
