import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from backend.database.connection import SessionLocal
from backend.models.host import Host

def update_host_ips():
    db = SessionLocal()
    try:
        # 1. Update gestivaone.com
        h1 = db.query(Host).filter(Host.hostname == "gestivaone.com").first()
        if h1:
            print(f"[*] Updating gestivaone.com IP from {h1.ip} to 216.198.79.1")
            h1.ip = "216.198.79.1"
            h1.notes = "Main production domain for Gestiva One. Monitored via HTTPS, Ping, and SSL/TLS checks."
            
        # 2. Update festa.gestivaone.com
        h2 = db.query(Host).filter(Host.hostname == "festa.gestivaone.com").first()
        if h2:
            print(f"[*] Updating festa.gestivaone.com IP from {h2.ip} to 64.29.17.65")
            h2.ip = "64.29.17.65"
            h2.notes = "Gestiva Festa events subdomain."

        # 3. Update gestivaone-store.vercel.app
        h3 = db.query(Host).filter(Host.hostname == "gestivaone-store.vercel.app").first()
        if h3:
            print(f"[*] Updating gestivaone-store.vercel.app IP from {h3.ip} to 64.29.17.67")
            h3.ip = "64.29.17.67"
            h3.notes = "Gestiva One Store application."

        db.commit()
        print("[+] IP addresses successfully updated in database inventory!")
    except Exception as e:
        db.rollback()
        print(f"[-] Failed to update host IPs: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    update_host_ips()
