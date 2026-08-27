from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
import datetime
from backend.database.connection import get_db
from backend.models.history import History
from backend.models.host import Host

router = APIRouter(prefix="/history", tags=["History"])

@router.get("")
def get_history_metrics(
    host_id: int,
    metric_name: str,
    timeframe: str = Query("24h", regex="^(24h|7d|30d|90d)$"),
    db: Session = Depends(get_db)
):
    now = datetime.datetime.utcnow()
    
    if timeframe == "24h":
        start_time = now - datetime.timedelta(hours=24)
    elif timeframe == "7d":
        start_time = now - datetime.timedelta(days=7)
    elif timeframe == "30d":
        start_time = now - datetime.timedelta(days=30)
    else:
        start_time = now - datetime.timedelta(days=90)
        
    metrics = db.query(History).filter(
        History.host_id == host_id,
        History.metric_name == metric_name,
        History.timestamp >= start_time
    ).order_by(History.timestamp.asc()).all()
    
    timestamps = [m.timestamp.isoformat() for m in metrics]
    values = [m.metric_value for m in metrics]
    
    return {
        "host_id": host_id,
        "metric_name": metric_name,
        "timeframe": timeframe,
        "timestamps": timestamps,
        "values": values
    }
