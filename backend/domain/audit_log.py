"""
Gestiva Security (GestivaSec V1) — SLICE-008: Audit Log Domain Model
Encapsulates Administrative Action Audit Events and Inmutability Rules (BR-0004 & BR-0005).
"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, Optional

@dataclass(frozen=True)
class AuditEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str = ""
    actor_user_id: str = ""
    actor_email: str = ""
    action: str = ""
    resource_type: str = ""
    resource_id: str = ""
    details: Dict[str, Any] = field(default_factory=dict)
    ip_address: str = "127.0.0.1"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
