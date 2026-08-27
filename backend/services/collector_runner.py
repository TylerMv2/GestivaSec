import time
import threading
import logging
from backend.database.connection import SessionLocal
from backend.models.settings import SettingsModel
from backend.collectors import (
    PingCollector, DNSCollector, HTTPCollector, HTTPSCollector,
    TLSCollector, SSHCollector, PortCollector, SystemCollector,
    TrafficCollector, InventoryCollector
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CollectorRunner")

class CollectorRunner:
    def __init__(self):
        self._running = False
        self._threads = []
        self.collectors_classes = {
            "PingCollector": PingCollector,
            "DNSCollector": DNSCollector,
            "HTTPCollector": HTTPCollector,
            "HTTPSCollector": HTTPSCollector,
            "TLSCollector": TLSCollector,
            "SSHCollector": SSHCollector,
            "PortCollector": PortCollector,
            "SystemCollector": SystemCollector,
            "TrafficCollector": TrafficCollector,
            "InventoryCollector": InventoryCollector
        }
        self.active_threads = {}

    def _run_collector_loop(self, collector_name: str, collector_cls):
        """Runs an individual collector on a loop matching its configured interval"""
        logger.info(f"Starting background loop for {collector_name}")
        
        while self._running:
            db = SessionLocal()
            try:
                # Check current configuration in database
                setting = db.query(SettingsModel).filter(SettingsModel.module_name == collector_name).first()
                
                if setting and setting.enabled:
                    interval = setting.interval_seconds
                    db.close() # Close session before collector runs its own session
                    
                    # Instantiate and run
                    collector = collector_cls()
                    try:
                        logger.debug(f"Running collector: {collector_name}")
                        collector.run()
                    except Exception as e:
                        logger.error(f"Error running collector {collector_name}: {e}", exc_info=True)
                    finally:
                        collector.close()
                else:
                    interval = 10 # Check settings table again in 10 seconds if disabled
                    db.close()
                    
            except Exception as e:
                logger.error(f"Database error in runner loop for {collector_name}: {e}")
                interval = 10
                db.close()

            # Sleep in small increments to respond quickly to shutdown requests
            for _ in range(interval):
                if not self._running:
                    break
                time.sleep(1)
                
        logger.info(f"Stopped background loop for {collector_name}")

    def start(self):
        """Starts all collector threads"""
        if self._running:
            return
            
        self._running = True
        logger.info("Initializing Gestiva Observability Collector Runner...")
        
        for name, cls in self.collectors_classes.items():
            t = threading.Thread(
                target=self._run_collector_loop,
                args=(name, cls),
                name=f"Thread-{name}",
                daemon=True
            )
            self.active_threads[name] = t
            t.start()

    def stop(self):
        """Signals runner shutdown"""
        self._running = False
        logger.info("Stopping Gestiva Observability Collector Runner...")
        
        # Wait for threads to terminate
        for name, t in self.active_threads.items():
            t.join(timeout=2)
            
        self.active_threads.clear()
        logger.info("All collector loops stopped.")

# Global shared instance
collector_runner_service = CollectorRunner()
