import psutil
import time
import datetime
from backend.collectors.base import BaseCollector
from backend.models.host import Host

class SystemCollector(BaseCollector):
    name = "SystemCollector"

    def run(self):
        if not self.is_enabled():
            return

        # Find the Localhost record
        localhost = self.db.query(Host).filter(Host.ip == "127.0.0.1").first()
        if not localhost:
            # Self-heal and create localhost if missing
            localhost = Host(
                hostname="localhost",
                ip="127.0.0.1",
                os="Kali Linux",
                status="UP",
                classification="Server"
            )
            self.db.add(localhost)
            self.db.commit()

        # Gather resource telemetry using psutil
        cpu_percent = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        ram_percent = mem.percent
        disk = psutil.disk_usage('/')
        disk_percent = disk.percent
        
        # Calculate network throughput (delta bytes)
        net_start = psutil.net_io_counters()
        time.sleep(0.5)
        net_end = psutil.net_io_counters()
        
        bytes_sent_sec = net_end.bytes_sent - net_start.bytes_sent
        bytes_recv_sec = net_end.bytes_recv - net_start.bytes_recv
        total_throughput_kb = (bytes_sent_sec + bytes_recv_sec) / 1024.0 # KB/s

        # Get system boot time for Uptime
        boot_time_timestamp = psutil.boot_time()
        uptime_seconds = time.time() - boot_time_timestamp
        uptime_days = uptime_seconds / 86400.0

        # Save to database metrics
        self.save_metric(localhost.id, "CPU", cpu_percent)
        self.save_metric(localhost.id, "RAM", ram_percent)
        self.save_metric(localhost.id, "Disk", disk_percent)
        self.save_metric(localhost.id, "NetThroughput", total_throughput_kb)
        
        # CPU alerts
        cpu_alert_source = f"System_CPU_{localhost.id}"
        if cpu_percent > 90.0:
            self.raise_alert(
                host_id=localhost.id,
                level="Critical",
                source=cpu_alert_source,
                description=f"Localhost CPU utilization is CRITICAL: {cpu_percent:.2f}%"
            )
        elif cpu_percent > 80.0:
            self.raise_alert(
                host_id=localhost.id,
                level="Warning",
                source=cpu_alert_source,
                description=f"Localhost CPU utilization is HIGH: {cpu_percent:.2f}%"
            )
        else:
            self.resolve_alerts(localhost.id, cpu_alert_source)

        # RAM alerts
        ram_alert_source = f"System_RAM_{localhost.id}"
        if ram_percent > 90.0:
            self.raise_alert(
                host_id=localhost.id,
                level="Critical",
                source=ram_alert_source,
                description=f"Localhost Memory usage is CRITICAL: {ram_percent:.2f}%"
            )
        else:
            self.resolve_alerts(localhost.id, ram_alert_source)

        # Disk alerts
        disk_alert_source = f"System_Disk_{localhost.id}"
        if disk_percent > 90.0:
            self.raise_alert(
                host_id=localhost.id,
                level="Critical",
                source=disk_alert_source,
                description=f"Localhost Disk space is CRITICAL: {disk_percent:.2f}%"
            )
        else:
            self.resolve_alerts(localhost.id, disk_alert_source)

        self.log_message(
            host_id=localhost.id,
            ip=localhost.ip,
            message=f"Localhost system resources: CPU: {cpu_percent:.1f}%, RAM: {ram_percent:.1f}%, Disk: {disk_percent:.1f}%, Net: {total_throughput_kb:.2f} KB/s, Uptime: {uptime_days:.2f} days",
            level="Info",
            service="System"
        )
        
        # Update localhost status/latency
        localhost.status = "UP"
        localhost.latency_ms = 0.05
        self.db.commit()

if __name__ == "__main__":
    collector = SystemCollector()
    try:
        collector.run()
    finally:
        collector.close()
