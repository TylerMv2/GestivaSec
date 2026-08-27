from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json
from backend.database.connection import get_db
from backend.models.service import Service
from backend.models.host import Host

router = APIRouter(prefix="/services", tags=["Services"])

@router.get("")
def get_services(db: Session = Depends(get_db)):
    services = db.query(Service).all()
    results = []
    
    for s in services:
        host = db.query(Host).filter(Host.id == s.host_id).first()
        hostname = host.hostname if host else "Unknown"
        
        try:
            meta = json.loads(s.metadata_json or "{}")
        except Exception:
            meta = {}

        results.append({
            "id": s.id,
            "host_id": s.host_id,
            "hostname": hostname,
            "name": s.name,
            "port": s.port,
            "status": s.status,
            "response_time_ms": round(s.response_time_ms, 2),
            "version": s.version,
            "last_check": s.last_check.isoformat(),
            "metadata": meta
        })
        
    return results
