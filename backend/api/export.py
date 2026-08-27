from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
import io
import json
import pandas as pd
from backend.database.connection import get_db
from backend.models.host import Host
from backend.models.service import Service
from backend.models.alert import Alert
from backend.models.traffic import Traffic
from backend.models.log import Log

router = APIRouter(prefix="/export", tags=["Export"])

@router.get("/csv")
def export_csv(
    table: str = Query("hosts", regex="^(hosts|services|alerts|traffic|logs)$"),
    db: Session = Depends(get_db)
):
    # Select table
    if table == "hosts":
        data = db.query(Host).all()
        list_dicts = [{
            "id": h.id, "hostname": h.hostname, "ip": h.ip, "os": h.os,
            "status": h.status, "latency_ms": h.latency_ms,
            "classification": h.classification, "notes": h.notes
        } for h in data]
    elif table == "services":
        data = db.query(Service).all()
        list_dicts = [{
            "id": s.id, "host_id": s.host_id, "name": s.name, "port": s.port,
            "status": s.status, "response_time_ms": s.response_time_ms,
            "version": s.version, "last_check": s.last_check
        } for s in data]
    elif table == "alerts":
        data = db.query(Alert).all()
        list_dicts = [{
            "id": a.id, "timestamp": a.timestamp, "level": a.level, "source": a.source,
            "description": a.description, "status": a.status, "resolved_at": a.resolved_at
        } for a in data]
    elif table == "traffic":
        data = db.query(Traffic).all()
        list_dicts = [{
            "id": t.id, "timestamp": t.timestamp, "protocol": t.protocol, "port": t.port,
            "source_ip": t.source_ip, "dest_ip": t.dest_ip, "source_port": t.source_port,
            "dest_port": t.dest_port, "volume_bytes": t.volume_bytes,
            "latency_ms": t.latency_ms, "connection_state": t.connection_state
        } for t in data]
    else: # logs
        data = db.query(Log).all()
        list_dicts = [{
            "id": l.id, "timestamp": l.timestamp, "source_ip": l.source_ip,
            "level": l.level, "service": l.service, "message": l.message
        } for l in data]

    if not list_dicts:
        raise HTTPException(status_code=404, detail="No data available to export")

    # Generate CSV in memory using pandas
    df = pd.DataFrame(list_dicts)
    stream = io.StringIO()
    df.to_csv(stream, index=False)
    
    # Return as StreamingResponse
    response = StreamingResponse(
        io.BytesIO(stream.getvalue().encode("utf-8")),
        media_type="text/csv"
    )
    response.headers["Content-Disposition"] = f"attachment; filename=gestiva_{table}_export.csv"
    return response

@router.get("/json")
def export_json(
    table: str = Query("hosts", regex="^(hosts|services|alerts|traffic|logs)$"),
    db: Session = Depends(get_db)
):
    if table == "hosts":
        data = db.query(Host).all()
        list_dicts = [{
            "id": h.id, "hostname": h.hostname, "ip": h.ip, "os": h.os,
            "status": h.status, "latency_ms": h.latency_ms,
            "classification": h.classification, "notes": h.notes
        } for h in data]
    elif table == "services":
        data = db.query(Service).all()
        list_dicts = [{
            "id": s.id, "host_id": s.host_id, "name": s.name, "port": s.port,
            "status": s.status, "response_time_ms": s.response_time_ms,
            "version": s.version, "last_check": s.last_check.isoformat()
        } for s in data]
    elif table == "alerts":
        data = db.query(Alert).all()
        list_dicts = [{
            "id": a.id, "timestamp": a.timestamp.isoformat(), "level": a.level, "source": a.source,
            "description": a.description, "status": a.status, "resolved_at": a.resolved_at.isoformat() if a.resolved_at else None
        } for a in data]
    elif table == "traffic":
        data = db.query(Traffic).all()
        list_dicts = [{
            "id": t.id, "timestamp": t.timestamp.isoformat(), "protocol": t.protocol, "port": t.port,
            "source_ip": t.source_ip, "dest_ip": t.dest_ip, "source_port": t.source_port,
            "dest_port": t.dest_port, "volume_bytes": t.volume_bytes,
            "latency_ms": t.latency_ms, "connection_state": t.connection_state
        } for t in data]
    else: # logs
        data = db.query(Log).all()
        list_dicts = [{
            "id": l.id, "timestamp": l.timestamp.isoformat(), "source_ip": l.source_ip,
            "level": l.level, "service": l.service, "message": l.message
        } for l in data]

    if not list_dicts:
        raise HTTPException(status_code=404, detail="No data available to export")

    # Generate JSON response
    response_data = json.dumps(list_dicts, indent=2)
    response = StreamingResponse(
        io.BytesIO(response_data.encode("utf-8")),
        media_type="application/json"
    )
    response.headers["Content-Disposition"] = f"attachment; filename=gestiva_{table}_export.json"
    return response
