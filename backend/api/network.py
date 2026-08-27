from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import json
from backend.database.connection import get_db
from backend.models.host import Host
from backend.models.service import Service

router = APIRouter(prefix="/network", tags=["Network"])

@router.get("")
def get_network_status(db: Session = Depends(get_db)):
    hosts = db.query(Host).all()
    network_data = []
    
    total_latency = 0.0
    valid_latencies = 0
    total_packet_loss = 0.0
    
    for host in hosts:
        # Load authorized ports safely
        try:
            ports = json.loads(host.ports_authorized or "[]")
        except Exception:
            ports = []

        # Count services of this host
        svcs = db.query(Service).filter(Service.host_id == host.id).all()
        svcs_list = [{"name": s.name, "port": s.port, "status": s.status, "response_time": s.response_time_ms} for s in svcs]
        
        # Calculate stats
        if host.status == "UP":
            total_latency += host.latency_ms
            valid_latencies += 1
            loss = 0.0
        else:
            loss = 100.0
        total_packet_loss += loss

        network_data.append({
            "id": host.id,
            "hostname": host.hostname,
            "ip": host.ip,
            "status": host.status,
            "latency_ms": round(host.latency_ms, 2),
            "packet_loss": loss,
            "ports_authorized": ports,
            "classification": host.classification,
            "services": svcs_list,
            "tags": json.loads(host.tags or "[]"),
            "updated_at": host.updated_at.isoformat()
        })

    avg_latency = (total_latency / valid_latencies) if valid_latencies > 0 else 0.0
    avg_packet_loss = (total_packet_loss / len(hosts)) if len(hosts) > 0 else 0.0

    return {
        "avg_latency_ms": round(avg_latency, 2),
        "avg_packet_loss_percent": round(avg_packet_loss, 2),
        "hosts": network_data
    }
