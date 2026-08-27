"""
Gestiva Security (GestivaSec V1) — Audit Log REST API Router (SLICE-008)
Exposes GET /api/v1/audit and /api/v1/audit/logs for organization audit events.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status, Header
from pydantic import BaseModel

from backend.application.audit_service import AuditService
from backend.application.auth_service import AuthenticationService

router = APIRouter(prefix="/api/v1/audit", tags=["Audit Log"])
audit_service = AuditService()
auth_service = AuthenticationService()

class AuditEventResponse(BaseModel):
    event_id: str
    organization_id: str
    actor_user_id: str
    actor_email: str
    action: str
    resource_type: str
    resource_id: str
    ip_address: str
    timestamp: str

@router.get("", response_model=List[AuditEventResponse])
@router.get("/", response_model=List[AuditEventResponse])
@router.get("/logs", response_model=List[AuditEventResponse])
@router.get("/log", response_model=List[AuditEventResponse])
async def list_audit_logs(
    authorization: Optional[str] = Header(None),
    x_organization_id: Optional[str] = Header(None)
):
    """Returns audit log entries for the tenant organization (BR-0004)."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Header Authorization Bearer requerido.")

    token = authorization.split(" ")[1]
    user = await auth_service.verify_token(token)
    if not user:
        raise HTTPException(status_code=401, detail="Token JWT inválido o revocado.")

    org_id = x_organization_id or user.organization_id
    events = await audit_service.list_organization_logs(org_id)

    return [
        AuditEventResponse(
            event_id=e.event_id,
            organization_id=e.organization_id,
            actor_user_id=e.actor_user_id,
            actor_email=e.actor_email,
            action=e.action,
            resource_type=e.resource_type,
            resource_id=e.resource_id,
            ip_address=e.ip_address,
            timestamp=e.timestamp.isoformat()
        )
        for e in events
    ]
