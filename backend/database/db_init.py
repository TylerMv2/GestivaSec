import sys
import json
import datetime
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from backend.database.connection import engine, Base, SessionLocal
from backend.models.host import Host
from backend.models.service import Service
from backend.models.user import User
from backend.models.settings import SettingsModel
from backend.models.config import Config
from backend.models.event import Event
from backend.infrastructure.asset_repository import AssetRepository
from backend.infrastructure.synthetic_repository import SyntheticRepository
from backend.infrastructure.audit_repository import AuditRepository

def init_db():
    print("[*] Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # Initialize in-memory and DB adapters
    AssetRepository()
    SyntheticRepository()
    AuditRepository()

    db = SessionLocal()
    try:
        # Check if users already exist
        if db.query(User).first() is not None:
            print("[*] Database already initialized and seeded.")
            return

        print("[*] Seeding default users (Admin, Operator, ReadOnly)...")
        # Admin / admin123
        admin_user = User(
            username="admin",
            password_hash=User.hash_password("admin123"),
            role="Admin",
            is_active=True
        )
        # Operator / operator123
        operator_user = User(
            username="operator",
            password_hash=User.hash_password("operator123"),
            role="Operator",
            is_active=True
        )
        # ReadOnly / read123
        readonly_user = User(
            username="readonly",
            password_hash=User.hash_password("read123"),
            role="ReadOnly",
            is_active=True
        )
        db.add_all([admin_user, operator_user, readonly_user])

        print("[*] Seeding target hosts (gestivaone.com, pay.gestivaone.com, Localhost)...")
        
        # Target 1: gestivaone.com
        gestiva_host = Host(
            hostname="gestivaone.com",
            ip="104.21.32.228",  # Cloudflare IP or standard lookup
            os="Linux (Cloudflare protected)",
            status="UP",
            latency_ms=14.5,
            ports_authorized=json.dumps([80, 443]),
            classification="Server",
            notes="Main production domain for Gestiva One. Monitored via HTTPS and SSL/TLS checks.",
            tags=json.dumps(["production", "external", "web"])
        )
        db.add(gestiva_host)
        db.flush()  # Populates ID
        
        # Target 2: pay.gestivaone.com
        pay_host = Host(
            hostname="pay.gestivaone.com",
            ip="104.21.32.229",
            os="Linux (Cloudflare protected)",
            status="UP",
            latency_ms=18.2,
            ports_authorized=json.dumps([443]),
            classification="Server",
            notes="Payment Gateway production endpoint for Gestiva One.",
            tags=json.dumps(["production", "payments", "external"])
        )
        db.add(pay_host)
        db.flush()

        # Target 3: Localhost
        localhost_host = Host(
            hostname="localhost",
            ip="127.0.0.1",
            os="Linux Server",
            status="UP",
            latency_ms=0.1,
            ports_authorized=json.dumps([22, 80, 443, 8000]),
            classification="Server",
            notes="Local operations host where Gestiva Security runs.",
            tags=json.dumps(["local", "development"])
        )
        db.add(localhost_host)
        db.flush()

        # Seed services for gestivaone.com
        gestiva_http = Service(
            host_id=gestiva_host.id,
            name="HTTP",
            port=80,
            status="UP",
            response_time_ms=15.0,
            version="Cloudflare HTTP server",
            last_check=datetime.datetime.utcnow(),
            metadata_json=json.dumps({"description": "Redirects to HTTPS"})
        )
        gestiva_https = Service(
            host_id=gestiva_host.id,
            name="HTTPS",
            port=443,
            status="UP",
            response_time_ms=14.5,
            version="Cloudflare HTTP server",
            last_check=datetime.datetime.utcnow(),
            metadata_json=json.dumps({"ssl_enabled": True})
        )
        gestiva_dns = Service(
            host_id=gestiva_host.id,
            name="DNS",
            port=53,
            status="UP",
            response_time_ms=5.0,
            version="Cloudflare Authoritative DNS",
            last_check=datetime.datetime.utcnow(),
            metadata_json=json.dumps({"dnssec": True})
        )
        db.add_all([gestiva_http, gestiva_https, gestiva_dns])

        # Seed services for Localhost
        local_ssh = Service(
            host_id=localhost_host.id,
            name="SSH",
            port=22,
            status="UP",
            response_time_ms=1.2,
            version="OpenSSH 9.6",
            last_check=datetime.datetime.utcnow()
        )
        local_http = Service(
            host_id=localhost_host.id,
            name="HTTP (GestivaSec Panel)",
            port=8000,
            status="UP",
            response_time_ms=0.5,
            version="FastAPI Uvicorn",
            last_check=datetime.datetime.utcnow()
        )
        db.add_all([local_ssh, local_http])

        print("[*] Seeding collector settings...")
        collectors = [
            "PingCollector", "DNSCollector", "HTTPCollector", "HTTPSCollector", 
            "TLSCollector", "SSHCollector", "PortCollector", 
            "InventoryCollector", "TrafficCollector", "SystemCollector"
        ]
        for col in collectors:
            set_model = SettingsModel(
                module_name=col,
                enabled=True,
                interval_seconds=30 if col != "InventoryCollector" else 300,
                configuration=json.dumps({
                    "timeout": 5,
                    "retries": 2
                })
            )
            db.add(set_model)

        print("[*] Seeding global config...")
        configs = {
            "site_name": "Gestiva Security SOC Dashboard",
            "retention_days": "90",
            "cyberpunk_theme_active": "true"
        }
        for k, v in configs.items():
            db.add(Config(key=k, value=v, description=f"System setting: {k}"))

        # Add initial system event
        db.add(Event(
            type="System",
            source="Database Initializer",
            message="Database successfully created and seeded with default GestivaOne targets.",
            details=json.dumps({"status": "success", "timestamp": str(datetime.datetime.utcnow())})
        ))

        db.commit()
        print("[+] Database initialization complete!")
    except Exception as e:
        db.rollback()
        print(f"[-] Database seed failed: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
