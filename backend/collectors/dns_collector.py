import time
import socket
import datetime
from backend.collectors.base import BaseCollector
from backend.models.host import Host
from backend.models.service import Service

class DNSCollector(BaseCollector):
    name = "DNSCollector"

    def _resolve_dns(self, hostname: str) -> tuple[bool, float, str]:
        """
        Resolves a hostname to IP.
        Returns: (success, latency_ms, ip_resolved)
        """
        start = time.time()
        try:
            resolved_ip = socket.gethostbyname(hostname)
            latency = (time.time() - start) * 1000
            return True, latency, resolved_ip
        except Exception as e:
            return False, 0.0, str(e)

    def run(self):
        if not self.is_enabled():
            return

        # Query all hosts that have DNS service mapped, or domains in the config
        # Let's check DNS services in our database
        dns_services = self.db.query(Service).filter(Service.name == "DNS").all()
        
        for service in dns_services:
            host = service.host
            success, latency, result = self._resolve_dns(host.hostname)
            
            service.last_check = datetime.datetime.utcnow()
            if success:
                service.status = "UP"
                service.response_time_ms = latency
                self.resolve_alerts(host.id, f"DNS_{service.id}")
                self.save_metric(host.id, "DNSErrors", 0.0)
                self.log_message(host.id, host.ip, f"DNS resolution for {host.hostname} succeeded: {result} in {latency:.2f}ms", "Info", "DNS")
            else:
                service.status = "DOWN"
                service.response_time_ms = 0.0
                self.raise_alert(
                    host_id=host.id,
                    level="Important",
                    source=f"DNS_{service.id}",
                    description=f"DNS resolution failed for {host.hostname}. Error: {result}"
                )
                self.save_metric(host.id, "DNSErrors", 1.0)
                self.log_message(host.id, host.ip, f"DNS resolution failed for {host.hostname}: {result}", "Warn", "DNS")
            
            self.db.commit()

if __name__ == "__main__":
    collector = DNSCollector()
    try:
        collector.run()
    finally:
        collector.close()
