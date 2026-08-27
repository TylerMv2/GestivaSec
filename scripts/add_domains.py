import json
import datetime
import socket
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.database.connection import SessionLocal
from backend.models.host import Host
from backend.models.service import Service

def resolve_ip(hostname: str, default: str) -> str:
    try:
        return socket.gethostbyname(hostname)
    except Exception:
        return default

def add_new_domains():
    db = SessionLocal()
    try:
        # Check if already added
        h1_exists = db.query(Host).filter(Host.hostname == "gestivaone-store.vercel.app").first()
        h2_exists = db.query(Host).filter(Host.hostname == "festa.gestivaone.com").first()
        
        if h1_exists and h2_exists:
            print("[*] Hostnames already present in database inventory.")
            return

        print("[*] Resolving real IPs for new domains...")
        ip_store = resolve_ip("gestivaone-store.vercel.app", "76.76.21.21")
        ip_festa = resolve_ip("festa.gestivaone.com", "104.21.32.228")

        # 1. Add gestivaone-store.vercel.app
        if not h1_exists:
            print("[*] Registering gestivaone-store.vercel.app...")
            host1 = Host(
                hostname="gestivaone-store.vercel.app",
                ip=ip_store,
                os="Linux (Vercel Edge Network)",
                status="UNKNOWN",
                ports_authorized=json.dumps([80, 443]),
                classification="Server",
                notes="Gestiva One Store application hosted on Vercel.",
                tags=json.dumps(["external", "store", "vercel"])
            )
            db.add(host1)
            db.flush()

            svc1_http = Service(
                host_id=host1.id,
                name="HTTP",
                port=80,
                status="DOWN",
                last_check=datetime.datetime.utcnow()
            )
            svc1_https = Service(
                host_id=host1.id,
                name="HTTPS",
                port=443,
                status="DOWN",
                last_check=datetime.datetime.utcnow()
            )
            db.add_all([svc1_http, svc1_https])

        # 2. Add festa.gestivaone.com
        if not h2_exists:
            print("[*] Registering festa.gestivaone.com...")
            host2 = Host(
                hostname="festa.gestivaone.com",
                ip=ip_festa,
                os="Linux (Cloudflare protected)",
                status="UNKNOWN",
                ports_authorized=json.dumps([80, 443]),
                classification="Server",
                notes="Gestiva Festa event portal.",
                tags=json.dumps(["external", "events", "cloudflare"])
            )
            db.add(host2)
            db.flush()

            svc2_http = Service(
                host_id=host2.id,
                name="HTTP",
                port=80,
                status="DOWN",
                last_check=datetime.datetime.utcnow()
            )
            svc2_https = Service(
                host_id=host2.id,
                name="HTTPS",
                port=443,
                status="DOWN",
                last_check=datetime.datetime.utcnow()
            )
            svc2_dns = Service(
                host_id=host2.id,
                name="DNS",
                port=53,
                status="DOWN",
                last_check=datetime.datetime.utcnow()
            )
            db.add_all([svc2_http, svc2_https, svc2_dns])

        db.commit()
        print("[+] New domains successfully registered in database inventory!")
    except Exception as e:
        db.rollback()
        print(f"[-] Failed to add domains: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_new_domains()
