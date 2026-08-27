import time
import requests
import datetime
import json
from backend.collectors.base import BaseCollector
from backend.models.service import Service

class HTTPCollector(BaseCollector):
    name = "HTTPCollector"

    def _check_http(self, ip: str, port: int, hostname: str) -> tuple[bool, float, int, str]:
        """
        Performs an HTTP check on a host.
        Returns: (success, latency_ms, status_code, server_header)
        """
        # Formulate check URL - use hostname if possible, fallback to IP
        url = f"http://{hostname}:{port}/" if hostname else f"http://{ip}:{port}/"
        start = time.time()
        try:
            # We set allow_redirects=True to test standard path, but cap timeout to 5 seconds
            res = requests.get(url, timeout=5, headers={"User-Agent": "GestivaObservability/1.0"})
            latency = (time.time() - start) * 1000
            server = res.headers.get("Server", "Unknown")
            return True, latency, res.status_code, server
        except Exception as e:
            return False, 0.0, 0, str(e)

    def run(self):
        if not self.is_enabled():
            return

        # Query HTTP services
        http_services = self.db.query(Service).filter(Service.name == "HTTP").all()
        
        for service in http_services:
            host = service.host
            success, latency, status_code, server = self._check_http(host.ip, service.port, host.hostname)
            
            service.last_check = datetime.datetime.utcnow()
            meta = json.loads(service.metadata_json or "{}")
            meta["status_code"] = status_code
            meta["server"] = server
            service.metadata_json = json.dumps(meta)
            
            if success and status_code < 500:
                service.status = "UP"
                service.response_time_ms = latency
                if server != "Unknown":
                    service.version = server
                self.resolve_alerts(host.id, f"HTTP_{service.id}")
                self.log_message(host.id, host.ip, f"HTTP check on port {service.port} succeeded (Status: {status_code}) in {latency:.2f}ms", "Info", "HTTP")
            else:
                service.status = "DOWN"
                service.response_time_ms = 0.0
                self.raise_alert(
                    host_id=host.id,
                    level="Warning" if status_code >= 500 else "Critical",
                    source=f"HTTP_{service.id}",
                    description=f"HTTP service on port {service.port} is down or returned error status {status_code}. Details: {server}"
                )
                self.log_message(host.id, host.ip, f"HTTP check on port {service.port} failed. Code: {status_code}, Error: {server}", "Error", "HTTP")
            
            self.db.commit()

if __name__ == "__main__":
    collector = HTTPCollector()
    try:
        collector.run()
    finally:
        collector.close()
