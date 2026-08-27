from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
import datetime
import json
from backend.database.connection import get_db
from backend.models.host import Host
from backend.models.service import Service
from backend.models.alert import Alert
from backend.models.history import History

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("")
def get_dashboard_data(db: Session = Depends(get_db)):
    # 1. Total hosts & availability
    total_hosts = db.query(Host).count()
    up_hosts = db.query(Host).filter(Host.status == "UP").count()
    availability = (up_hosts / total_hosts * 100.0) if total_hosts > 0 else 100.0

    # 2. Active services count
    active_services = db.query(Service).filter(Service.status == "UP").count()
    total_services = db.query(Service).count()

    # 3. Active alerts count by severity
    active_alerts = db.query(Alert).filter(Alert.status == "Active").all()
    alert_counts = {"Critical": 0, "Important": 0, "Warning": 0, "Info": 0}
    for alert in active_alerts:
        if alert.level in alert_counts:
            alert_counts[alert.level] += 1

    # 4. Fetch latest system utilization (Localhost metrics)
    localhost = db.query(Host).filter(Host.ip == "127.0.0.1").first()
    system_metrics = {"cpu": 0.0, "ram": 0.0, "disk": 0.0, "net": 0.0}
    
    if localhost:
        # Query latest metric of each type
        for metric_name in ["CPU", "RAM", "Disk", "NetThroughput"]:
            latest_metric = db.query(History).filter(
                History.host_id == localhost.id,
                History.metric_name == metric_name
            ).order_by(History.timestamp.desc()).first()
            if latest_metric:
                system_metrics[metric_name.lower().replace("netthroughput", "net")] = latest_metric.metric_value

    # 5. Fetch 5 most recent active alerts
    recent_alerts = db.query(Alert).filter(Alert.status == "Active").order_by(Alert.timestamp.desc()).limit(5).all()
    formatted_alerts = []
    for a in recent_alerts:
        formatted_alerts.append({
            "id": a.id,
            "timestamp": a.timestamp.isoformat(),
            "level": a.level,
            "source": a.source,
            "description": a.description
        })

    return {
        "status": "UP" if alert_counts["Critical"] == 0 else "DEGRADED",
        "availability_percent": round(availability, 2),
        "total_hosts": total_hosts,
        "up_hosts": up_hosts,
        "active_services": active_services,
        "total_services": total_services,
        "alert_counts": alert_counts,
        "system_metrics": system_metrics,
        "recent_alerts": formatted_alerts,
        "last_update": datetime.datetime.utcnow().isoformat()
    }
