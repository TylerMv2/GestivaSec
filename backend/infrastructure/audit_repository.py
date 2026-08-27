"""
Gestiva Security (GestivaSec V1) — Audit Log Repository Infrastructure Adapter
Append-only persistence for Audit Events (BR-0004 & BR-0005).
"""
from typing import List
from datetime import datetime
from backend.domain.audit_log import AuditEvent

_AUDIT_EVENTS: List[AuditEvent] = []

class AuditRepository:
    def __init__(self):
        if not _AUDIT_EVENTS:
            default_org = "00000000-0000-0000-0000-000000000001"
            now = datetime.utcnow()
            _AUDIT_EVENTS.extend([
                AuditEvent(
                    event_id="audit-evt-001",
                    organization_id=default_org,
                    actor_user_id="user-admin-01",
                    actor_email="ops@gestivaone.com",
                    action="SYSTEM_STARTUP",
                    resource_type="SOC_KERNEL",
                    resource_id="KERNEL-V1",
                    ip_address="127.0.0.1",
                    timestamp=now
                ),
                AuditEvent(
                    event_id="audit-evt-002",
                    organization_id=default_org,
                    actor_user_id="user-admin-01",
                    actor_email="ops@gestivaone.com",
                    action="ASSET_DISCOVERY_SCAN",
                    resource_type="DIGITAL_ASSET",
                    resource_id="https://gestivaone.com",
                    ip_address="127.0.0.1",
                    timestamp=now
                ),
                AuditEvent(
                    event_id="audit-evt-003",
                    organization_id=default_org,
                    actor_user_id="user-analyst-02",
                    actor_email="analyst@gestivaone.com",
                    action="SYNTHETIC_PROBE_EVALUATION",
                    resource_type="PROBE_SERVICE",
                    resource_id="11111111-1111-1111-1111-111111111111",
                    ip_address="127.0.0.1",
                    timestamp=now
                )
            ])

    async def record_event(self, event: AuditEvent) -> AuditEvent:
        """Appends audit event to storage."""
        _AUDIT_EVENTS.append(event)
        return event

    async def get_events_by_organization(self, organization_id: str) -> List[AuditEvent]:
        """Returns events filtered strictly by organization_id (BR-0004)."""
        return [e for e in _AUDIT_EVENTS if e.organization_id == organization_id]
