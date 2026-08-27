from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_
import datetime
from backend.database.connection import get_db
from backend.models.log import Log
from backend.models.host import Host

router = APIRouter(prefix="/logs", tags=["Logs"])

@router.get("")
def query_logs(
    level: str | None = None,
    host_id: int | None = None,
    service: str | None = None,
    search: str | None = None,
    hide_internal: bool = Query(False),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db)
):
    query = db.query(Log)
    
    if hide_internal:
        # Exclude localhost traffic & internal loop logs
        query = query.filter(Log.source_ip != "127.0.0.1")
        query = query.filter(Log.source_ip != "localhost")
        query = query.filter(~Log.message.like("%starting background loop%"))
        query = query.filter(~Log.message.like("%collecting metrics%"))
        query = query.filter(~Log.message.like("%is UP. Latency%"))
        query = query.filter(~Log.message.like("%Background query failed%"))
        query = query.filter(~Log.message.like("%Initializing Gestiva%"))
        
    if level:
        query = query.filter(Log.level == level)
    if host_id:
        query = query.filter(Log.host_id == host_id)
    if service:
        query = query.filter(Log.service == service)
    if search:
        # Match search term in messages or raw logs
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                Log.message.like(search_filter),
                Log.raw_log.like(search_filter),
                Log.source_ip.like(search_filter)
            )
        )
        
    total_count = query.count()
    results = query.order_by(Log.timestamp.desc()).limit(limit).offset(offset).all()
    
    formatted_logs = []
    for log in results:
        # Load host hostname
        host = db.query(Host).filter(Host.id == log.host_id).first()
        hostname = host.hostname if host else "Unknown"
        
        formatted_logs.append({
            "id": log.id,
            "timestamp": log.timestamp.isoformat(),
            "host_id": log.host_id,
            "hostname": hostname,
            "source_ip": log.source_ip,
            "level": log.level,
            "service": log.service,
            "message": log.message,
            "raw_log": log.raw_log
        })
        
    return {
        "total": total_count,
        "limit": limit,
        "offset": offset,
        "logs": formatted_logs
    }
