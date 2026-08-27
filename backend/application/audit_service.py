"""
Gestiva Security (GestivaSec V1) — Audit Application Service
Orchestrates recording and querying of Audit Events (SLICE-008).
"""
from typing import List, Optional, Dict, Any
from backend.domain.audit_log import AuditEvent
from backend.infrastructure.audit_repository import AuditRepository

class AuditService:
    def __init__(self, repo: Optional[AuditRepository] = None):
        self.repo = repo or AuditRepository()

    async def log_action(
        self,
        organization_id: str,
        actor_user_id: str,
        actor_email: str,
        action: str,
        resource_type: str,
        resource_id: str,
        details: Optional[Dict[str, Any]] = None,
        ip_address: str = "127.0.0.1"
    ) -> AuditEvent:
        event = AuditEvent(
            organization_id=organization_id,
            actor_user_id=actor_user_id,
            actor_email=actor_email,
            action=action,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            ip_address=ip_address
        )
        return await self.repo.record_event(event)

    async def list_organization_logs(self, organization_id: str) -> List[AuditEvent]:
        return await self.repo.get_events_by_organization(organization_id)
