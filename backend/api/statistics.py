from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
import datetime
from backend.database.connection import get_db
from backend.models.history import History
from backend.models.host import Host

router = APIRouter(prefix="/statistics", tags=["Statistics"])

def calculate_trend(values: list[float]) -> str:
    """Calculates directional trend (GROWING, STABLE, DECREASING) from a series of values"""
    if len(values) < 3:
        return "STABLE"
    
    # Calculate simple slope between start and end
    # Or average difference
    diffs = [values[i] - values[i-1] for i in range(1, len(values))]
    avg_diff = sum(diffs) / len(diffs)
    
    if avg_diff > 0.5: # Threshold for positive trend
        return "GROWING"
    elif avg_diff < -0.5: # Threshold for negative trend
        return "DECREASING"
    return "STABLE"

@router.get("/trends")
def get_trends(db: Session = Depends(get_db)):
    hosts = db.query(Host).all()
    trends_report = {}
    
    now = datetime.datetime.utcnow()
    one_hour_ago = now - datetime.timedelta(hours=1)
    
    for host in hosts:
        host_trends = {}
        
        # Check trends for CPU, RAM, Disk, Latency
        for metric in ["CPU", "RAM", "Disk", "Latency", "DNSErrors"]:
            metrics = db.query(History).filter(
                History.host_id == host.id,
                History.metric_name == metric,
                History.timestamp >= one_hour_ago
            ).order_by(History.timestamp.asc()).all()
            
            vals = [m.metric_value for m in metrics]
            trend = calculate_trend(vals)
            
            # Form simple prediction
            prediction = "Normal"
            if metric == "Disk" and trend == "GROWING" and vals[-1] > 80.0:
                prediction = "Disk saturation risk within 24h"
            elif metric == "RAM" and trend == "GROWING" and vals[-1] > 85.0:
                prediction = "High paging risk"
            elif metric == "Latency" and trend == "GROWING":
                prediction = "Network congestion likelihood"
                
            host_trends[metric.lower()] = {
                "current": vals[-1] if vals else 0.0,
                "trend": trend,
                "prediction": prediction
            }
            
        trends_report[host.hostname] = host_trends
        
    return {
        "timestamp": now.isoformat(),
        "trends": trends_report
    }
