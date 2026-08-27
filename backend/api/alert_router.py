"""
Gestiva Security (GestivaSec V1) — Alert, Timeline & Incident Center REST API Router
Exposes /api/v1/alerts, /api/v1/timeline, /api/v1/incidents endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.application.alert_service import AlertApplicationService
from backend.domain.alert_engine import AlertSeverity, IncidentStatus

router = APIRouter(prefix="/api/v1", tags=["Alert Engine & SOC Incident Center"])
alert_service = AlertApplicationService()

class AlertSchema(BaseModel):
    id: str
    asset_id: str
    target_url: str
    rule_name: str
    severity: str
    message: str
    created_at: str

class TimelineSchema(BaseModel):
    id: str
    event_type: str
    source: str
    description: str
    severity: str
    timestamp: str

class IncidentSchema(BaseModel):
    id: str
    alert_id: str
    title: str
    severity: str
    status: str
    assigned_to: str
    notes: List[str]
    rca_report: Optional[str]
    created_at: str

class TransitionIncidentRequest(BaseModel):
    status: IncidentStatus
    rca_report: Optional[str] = None

@router.get("/alerts", response_model=List[AlertSchema])
async def list_alerts():
    alerts = await alert_service.list_alerts()
    return [
        AlertSchema(
            id=a.id,
            asset_id=a.asset_id,
            target_url=a.target_url,
            rule_name=a.rule_name,
            severity=a.severity.value,
            message=a.message,
            created_at=a.created_at.isoformat()
        )
        for a in alerts
    ]

@router.get("/timeline", response_model=List[TimelineSchema])
async def list_timeline_events():
    events = await alert_service.list_timeline()
    return [
        TimelineSchema(
            id=e.id,
            event_type=e.event_type,
            source=e.source,
            description=e.description,
            severity=e.severity,
            timestamp=e.timestamp.isoformat()
        )
        for e in events
    ]

@router.get("/incidents", response_model=List[IncidentSchema])
async def list_incidents():
    incidents = await alert_service.list_incidents()
    return [
        IncidentSchema(
            id=i.id,
            alert_id=i.alert_id,
            title=i.title,
            severity=i.severity.value,
            status=i.status.value,
            assigned_to=i.assigned_to,
            notes=i.notes,
            rca_report=i.rca_report,
            created_at=i.created_at.isoformat()
        )
        for i in incidents
    ]

@router.post("/incidents/{incident_id}/transition", response_model=IncidentSchema)
async def transition_incident(incident_id: str, req: TransitionIncidentRequest):
    try:
        inc = await alert_service.transition_incident(incident_id, req.status, req.rca_report)
        return IncidentSchema(
            id=inc.id,
            alert_id=inc.alert_id,
            title=inc.title,
            severity=inc.severity.value,
            status=inc.status.value,
            assigned_to=inc.assigned_to,
            notes=inc.notes,
            rca_report=inc.rca_report,
            created_at=inc.created_at.isoformat()
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
