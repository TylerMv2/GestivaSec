"""
Gestiva Security (GestivaSec V1) — Alert, Timeline & Incident Persistence Repository
"""
from typing import List, Optional
from datetime import datetime, timezone

from backend.domain.alert_engine import SecurityAlert, TimelineEvent, SOCIncident, AlertSeverity, IncidentStatus

class AlertRepository:
    def __init__(self):
        self._alerts: List[SecurityAlert] = []
        self._timeline: List[TimelineEvent] = []
        self._incidents: List[SOCIncident] = []
        self._seed_default_data()

    def _seed_default_data(self):
        now = datetime.now(timezone.utc)
        # Default Alert
        alert = SecurityAlert(
            id="alt-001",
            asset_id="11111111-1111-1111-1111-111111111111",
            target_url="https://gestivaone.com",
            rule_name="HTTP_STATUS_500",
            severity=AlertSeverity.CRITICAL,
            message="Servicio HTTP devolvió código de error 500 Internal Server Error",
            created_at=now
        )
        self._alerts.append(alert)

        # Default Incident
        inc = SOCIncident(
            id="inc-001",
            alert_id="alt-001",
            title="Falla Crítica de Disponibilidad en GestivaOne Core Portal",
            severity=AlertSeverity.CRITICAL,
            status=IncidentStatus.INVESTIGATING,
            assigned_to="analyst@gestivaone.com",
            notes=["Analista SOC asignado a la investigación del incidente."],
            created_at=now
        )
        self._incidents.append(inc)

        # Default Timeline Events
        self._timeline.append(TimelineEvent(
            id="tl-001",
            event_type="ALERT",
            source="AlertEngine",
            description="Alerta Crítica P1 emitida por falla en HTTP Status 500",
            severity="CRITICAL",
            timestamp=now
        ))

    async def save_alert(self, alert: SecurityAlert):
        self._alerts.insert(0, alert)
        self._timeline.insert(0, TimelineEvent(
            id=f"tl-{len(self._timeline)+1}",
            event_type="ALERT",
            source="AlertEngine",
            description=f"Alerta {alert.severity.value}: {alert.message}",
            severity=alert.severity.value,
            timestamp=alert.created_at
        ))

    async def list_alerts(self) -> List[SecurityAlert]:
        return self._alerts

    async def list_timeline(self) -> List[TimelineEvent]:
        return self._timeline

    async def save_incident(self, incident: SOCIncident):
        self._incidents.insert(0, incident)

    async def list_incidents(self) -> List[SOCIncident]:
        return self._incidents

    async def get_incident(self, incident_id: str) -> Optional[SOCIncident]:
        for inc in self._incidents:
            if inc.id == incident_id:
                return inc
        return None
