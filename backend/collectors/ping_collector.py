import time
import subprocess
import os
from backend.collectors.base import BaseCollector
from backend.models.host import Host

class PingCollector(BaseCollector):
    name = "PingCollector"

    def _ping_host(self, ip: str) -> float:
        """
        Pings a host and returns latency in milliseconds.
        Returns -1.0 if host is unreachable.
        Uses subprocess ping as a fallback to avoid raw socket permission issues.
        """
        # Try subprocess ping first because on Kali/Linux raw sockets for ping3 can require root
        try:
            # -c 1: 1 packet, -W 2: timeout 2 seconds
            start_time = time.time()
            res = subprocess.run(
                ["ping", "-c", "1", "-W", "2", ip],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            duration = (time.time() - start_time) * 1000
            
            if res.returncode == 0:
                # Try to parse the exact rtt from stdout if possible
                # e.g. "rtt min/avg/max/mdev = 0.045/0.045/0.045/0.000 ms"
                for line in res.stdout.splitlines():
                    if "rtt" in line or "round-trip" in line:
                        parts = line.split("=")[1].strip().split("/")
                        return float(parts[1]) # avg latency
                return duration
            return -1.0
        except Exception:
            # Fallback to ping3 just in case
            try:
                import ping3
                latency = ping3.ping(ip, timeout=2)
                if latency is not None and latency is not False:
                    return latency * 1000
            except Exception:
                pass
            return -1.0

    def run(self):
        if not self.is_enabled():
            return

        hosts = self.db.query(Host).all()
        for host in hosts:
            latency = self._ping_host(host.ip)
            
            if latency >= 0:
                # Host is UP
                host.status = "UP"
                host.latency_ms = latency
                self.resolve_alerts(host.id, "Ping")
                self.save_metric(host.id, "Latency", latency)
                self.save_metric(host.id, "PacketLoss", 0.0)
                self.log_message(host.id, host.ip, f"Host {host.hostname} ({host.ip}) is UP. Latency: {latency:.2f}ms", "Info", "Ping")
            else:
                # Host is DOWN
                host.status = "DOWN"
                host.latency_ms = 0.0
                self.raise_alert(
                    host_id=host.id,
                    level="Critical",
                    source="Ping",
                    description=f"Host {host.hostname} ({host.ip}) is unreachable via ICMP Ping."
                )
                self.save_metric(host.id, "PacketLoss", 100.0)
                self.log_message(host.id, host.ip, f"Host {host.hostname} ({host.ip}) is DOWN (ICMP timeout)", "Error", "Ping")
            
            self.db.commit()

if __name__ == "__main__":
    collector = PingCollector()
    try:
        collector.run()
    finally:
        collector.close()
