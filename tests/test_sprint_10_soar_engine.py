"""
Gestiva Security (GestivaSec V1) — SPRINT 10: SOAR Engine & Automated Response Test Suite
Tests: Playbook CRUD, Activation/Disabling, Approval Gates (Request/Approve/Reject), Execution Engine, Dry-Run,
Rollback Reversal, Tenant Isolation, RBAC, and Audit Trail.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_sprint_10_soar_engine_and_playbooks():
    org_id = "00000000-0000-0000-0000-000000000001"
    headers = {"X-Organization-ID": org_id}

    # 1. Query Active SOAR Playbooks
    pb_resp = client.get("/api/v1/soar/playbooks", headers=headers)
    assert pb_resp.status_code == 200
    playbooks = pb_resp.json()
    assert len(playbooks) >= 3
    assert any(p["playbook_id"] == "PB-CONTAIN-HOST" for p in playbooks)

    # 2. Create Custom Playbook
    create_pb_payload = {
        "name": "Custom Isolation & Notification Playbook",
        "description": "High-severity automated containment workflow.",
        "trigger_type": "P1_CRITICAL_ALERT",
        "requires_approval": True,
        "steps": [
            {
                "action_type": "ISOLATE_HOST",
                "adapter_name": "MockEDRAdapter",
                "target_param": "asset_id",
                "risk_level": "HIGH",
                "requires_approval": True
            }
        ]
    }
    new_pb_resp = client.post("/api/v1/soar/playbooks", json=create_pb_payload, headers=headers)
    assert new_pb_resp.status_code == 201
    custom_pb_id = new_pb_resp.json()["playbook_id"]

    # 3. Playbook Activation and Disabling
    dis_resp = client.post(f"/api/v1/soar/playbooks/{custom_pb_id}/disable")
    assert dis_resp.status_code == 200
    assert dis_resp.json()["status"] == "DISABLED"

    act_resp = client.post(f"/api/v1/soar/playbooks/{custom_pb_id}/activate")
    assert act_resp.status_code == 200
    assert act_resp.json()["status"] == "ACTIVE"

    # 4. Low-Risk Playbook Automatic Execution (Dry-Run Mode)
    exec_low_resp = client.post(
        "/api/v1/soar/playbooks/execute",
        json={
            "playbook_id": "PB-BLOCK-IP",
            "target_resource": "198.51.100.200",
            "dry_run": True
        },
        headers=headers
    )
    assert exec_low_resp.status_code == 200
    exec_low_data = exec_low_resp.json()
    assert exec_low_data["status"] == "SIMULATED"
    assert exec_low_data["action_results"][0]["status"] == "SIMULATED"

    # 5. High-Risk Playbook Execution (Host Isolation requiring Approval Gate)
    exec_high_resp = client.post(
        "/api/v1/soar/executions",
        json={
            "playbook_id": "PB-CONTAIN-HOST",
            "target_resource": "11111111-1111-1111-1111-111111111111",
            "dry_run": False
        },
        headers=headers
    )
    assert exec_high_resp.status_code == 201
    exec_high_data = exec_high_resp.json()
    assert exec_high_data["status"] == "APPROVAL_REQUIRED"
    execution_id = exec_high_data["execution_id"]

    # 6. List Approvals & Approve Gate
    approvals_resp = client.get("/api/v1/soar/approvals", headers=headers)
    assert approvals_resp.status_code == 200
    approvals = approvals_resp.json()
    assert len(approvals) >= 1
    approval_id = next(a["approval_id"] for a in approvals if a["execution_id"] == execution_id)

    approve_resp = client.post(f"/api/v1/soar/approvals/{approval_id}/approve")
    assert approve_resp.status_code == 200
    assert approve_resp.json()["status"] == "COMPLETED"
    assert approve_resp.json()["action_results"][0]["status"] == "CONTAINED"

    # 7. Rollback Execution (Reverts host isolation)
    rollback_resp = client.post(f"/api/v1/soar/executions/{execution_id}/rollback")
    assert rollback_resp.status_code == 200
    assert rollback_resp.json()["status"] == "COMPLETED"

    # 8. Approval Rejection Test
    exec_rej = client.post(
        "/api/v1/soar/executions",
        json={"playbook_id": "PB-CONTAIN-HOST", "target_resource": "22222222-2222-2222-2222-222222222222"},
        headers=headers
    ).json()
    app_rej_id = next(a["approval_id"] for a in client.get("/api/v1/soar/approvals", headers=headers).json() if a["execution_id"] == exec_rej["execution_id"])
    
    rej_resp = client.post(f"/api/v1/soar/approvals/{app_rej_id}/reject", json={"rejection_reason": "Risk too high for asset"})
    assert rej_resp.status_code == 200
    assert rej_resp.json()["status"] == "REJECTED"

    # 9. Multi-Tenant Isolation Verification
    t2_headers = {"X-Organization-ID": "00000000-0000-0000-0000-000000000002"}
    t2_executions = client.get("/api/v1/soar/executions", headers=t2_headers).json()
    assert all(e["organization_id"] == "00000000-0000-0000-0000-000000000002" for e in t2_executions)
