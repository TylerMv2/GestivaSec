from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import json
import datetime
from backend.database.connection import get_db
from backend.models.traffic import Traffic

router = APIRouter(prefix="/traffic", tags=["Traffic"])

@router.get("")
def get_traffic_data(limit: int = 100, db: Session = Depends(get_db)):
    # Fetch recent traffic logs
    flows = db.query(Traffic).order_by(Traffic.timestamp.desc()).limit(limit).all()
    
    formatted_flows = []
    protocol_stats = {}
    
    for f in flows:
        # Build protocol volume statistics
        if f.protocol not in protocol_stats:
            protocol_stats[f.protocol] = {"bytes": 0, "hits": 0}
        protocol_stats[f.protocol]["bytes"] += f.volume_bytes
        protocol_stats[f.protocol]["hits"] += 1
        
        try:
            meta = json.loads(f.metadata_json or "{}")
        except Exception:
            meta = {}

        formatted_flows.append({
            "id": f.id,
            "timestamp": f.timestamp.isoformat(),
            "protocol": f.protocol,
            "port": f.port,
            "source_ip": f.source_ip,
            "dest_ip": f.dest_ip,
            "source_port": f.source_port,
            "dest_port": f.dest_port,
            "volume_bytes": f.volume_bytes,
            "latency_ms": round(f.latency_ms, 2),
            "state": f.connection_state,
            "metadata": meta
        })

    # Convert protocol stats to list for easier chart loading
    proto_summary = []
    for k, v in protocol_stats.items():
        proto_summary.append({
            "protocol": k,
            "volume_bytes": v["bytes"],
            "hits": v["hits"]
        })
        
    # Sort protocol summary by volume
    proto_summary = sorted(proto_summary, key=lambda x: x["volume_bytes"], reverse=True)

    return {
        "recent_flows": formatted_flows,
        "protocol_summary": proto_summary,
        "server_time": datetime.datetime.utcnow().isoformat()
    }
