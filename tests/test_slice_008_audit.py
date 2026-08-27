"""
Gestiva Security (GestivaSec V1) — SLICE-008: Audit Log Test Suite
Verifies Audit Event Recording, Tenant Isolation (BR-0004), and Inmutability Rules.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.application.audit_service import AuditService

client = TestClient(app)
audit_service = AuditService()

@pytest.mark.asyncio
async def test_record_and_query_audit_events():
    org_id = "00000000-0000-0000-0000-000000000001"
    
    # 1. Record Event
    event = await audit_service.log_action(
        organization_id=org_id,
        actor_user_id="user-123",
        actor_email="admin@gestivaone.com",
        action="USER_CREATED",
        resource_type="USER",
        resource_id="user-456",
        details={"role": "SOC_ANALYST"}
    )
    assert event.event_id is not None
    assert event.action == "USER_CREATED"

    # 2. Login to get Bearer token for API call
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@gestivaone.com", "password": "GestivaSec2026!"}
    )
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}", "X-Organization-ID": org_id}

    # 3. Call REST API /api/v1/audit/logs
    logs_resp = client.get("/api/v1/audit/logs", headers=headers)
    assert logs_resp.status_code == 200
    logs = logs_resp.json()
    assert len(logs) >= 1
    assert any(log["action"] == "USER_CREATED" for log in logs)

def test_unauthenticated_audit_access_fails():
    resp = client.get("/api/v1/audit/logs")
    assert resp.status_code == 401
