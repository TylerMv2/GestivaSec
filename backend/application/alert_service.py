"""
Gestiva Security (GestivaSec V1) — Alert & Incident Center Application Service
Evaluates Configurable Alert Rules and Governs Incident Center Status Lifecycle.
"""
from typing import List, Optional
from datetime import datetime, timezone

from backend.domain.alert_engine import SecurityAlert, TimelineEvent, SOCIncident, AlertSeverity, IncidentStatus
from backend.infrastructure.alert_repository import AlertRepository

class AlertApplicationService:
    def __init__(self, repo: Optional[AlertRepository] = None):
        self.repo = repo or AlertRepository()

    async def list_alerts(self) -> List[SecurityAlert]:
        return await self.repo.list_alerts()

    async def list_timeline(self) -> List[TimelineEvent]:
        return await self.repo.list_timeline()

    async def list_incidents(self) -> List[SOCIncident]:
        return await self.repo.list_incidents()

    async def evaluate_rule(self, asset_id: str, target_url: str, rule_type: str, details: str) -> SecurityAlert:
        severity = AlertSeverity.INFO
        if rule_type == "TLS_EXPIRATION":
            severity = AlertSeverity.WARNING
        elif rule_type == "HTTP_500_ERROR":
            severity = AlertSeverity.CRITICAL
        elif rule_type == "NEW_SUBDOMAIN":
            severity = AlertSeverity.INFO
        elif rule_type == "HEADER_REMOVED":
            severity = AlertSeverity.HIGH

        alert = SecurityAlert(
            id=f"alt-{datetime.now().timestamp():.0f}",
            asset_id=asset_id,
            target_url=target_url,
            rule_name=rule_type,
            severity=severity,
            message=f"Regla [{rule_type}] activada: {details}",
            created_at=datetime.now(timezone.utc)
        )
        await self.repo.save_alert(alert)
        return alert

    async def transition_incident(self, incident_id: str, new_status: IncidentStatus, rca_report: Optional[str] = None) -> SOCIncident:
        inc = await self.repo.get_incident(incident_id)
        if not inc:
            raise ValueError(f"Incidente '{incident_id}' no encontrado.")
        
        inc.transition_status(new_status, rca_report)
        return inc
