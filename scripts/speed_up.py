import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.database.connection import SessionLocal
from backend.models.settings import SettingsModel

def speed_up_collectors():
    db = SessionLocal()
    try:
        # Update intervals to 3 seconds for critical/fast collectors
        fast_collectors = [
            "PingCollector", "HTTPCollector", "HTTPSCollector", 
            "TLSCollector", "TrafficCollector", "SystemCollector"
        ]
        
        for col_name in fast_collectors:
            setting = db.query(SettingsModel).filter(SettingsModel.module_name == col_name).first()
            if setting:
                print(f"[*] Speeding up {col_name} interval to 3 seconds...")
                setting.interval_seconds = 3
                
        # Keep port collector at 10s (too fast will cause scan locks) and others at 30s
        port_setting = db.query(SettingsModel).filter(SettingsModel.module_name == "PortCollector").first()
        if port_setting:
            port_setting.interval_seconds = 10
            
        db.commit()
        print("[+] Telemetry collector intervals successfully updated to near real-time!")
    except Exception as e:
        db.rollback()
        print(f"[-] Failed to update intervals: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    speed_up_collectors()
