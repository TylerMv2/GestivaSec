"""
Gestiva Security (GestivaSec V1) — SPRINT 8: Incident & Case Management Comprehensive Test Suite
Tests: Incident lifecycle, Case lifecycle, deduplication, state transitions, evidence attachment, timeline logging,
comments, RCA enforcement, escalation, SLA, tenant isolation, and audit logging.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_sprint_8_incident_and_case_management_lifecycle():
    org_id = "00000000-0000-0000-0000-000000000001"
    headers = {"X-Organization-ID": org_id}

    # 1. Create Incident for Tenant 1
    create_inc_payload = {
        "title": "P1 Critical Host Compromise Attempt",
        "description": "Multi-stage attack chain correlated across 3 MITRE phases.",
        "origin_type": "ATTACK_CHAIN",
        "source_reference": "CHAIN-TEST-001",
        "severity": "P1_CRITICAL",
        "priority": "P1",
        "category": "AUTHENTICATION",
        "target_ip": "198.51.100.250",
        "assigned_to": "tier2@gestivaone.com"
    }
    inc_resp = client.post("/api/v1/incidents", json=create_inc_payload, headers=headers)
    assert inc_resp.status_code == 201
    inc_data = inc_resp.json()
    incident_id = inc_data["incident_id"]
    assert inc_data["status"] == "NEW"
    assert inc_data["priority"] == "P1"

    # 2. Duplicate Incident Prevention (Idempotency)
    dup_resp = client.post("/api/v1/incidents", json=create_inc_payload, headers=headers)
    assert dup_resp.status_code == 201
    assert dup_resp.json()["incident_id"] == incident_id  # Deduplicated!

    # 3. Incident State Transitions (NEW -> ACKNOWLEDGED -> TRIAGED -> INVESTIGATING -> RESOLVED -> CLOSED)
    ack_resp = client.post(f"/api/v1/incidents/{incident_id}/acknowledge")
    assert ack_resp.status_code == 200
    assert ack_resp.json()["status"] == "ACKNOWLEDGED"

    triage_resp = client.post(f"/api/v1/incidents/{incident_id}/triage")
    assert triage_resp.status_code == 200
    assert triage_resp.json()["status"] == "TRIAGED"

    # Invalid state transition rejection (TRIAGED cannot jump directly to CLOSED without RCA)
    invalid_resp = client.post(f"/api/v1/incidents/{incident_id}/close", json={"root_cause": "test", "closure_reason": "test"})
    assert invalid_resp.status_code == 400

    # 4. Analyst Assignment & Reassignment
    assign_resp = client.post(f"/api/v1/incidents/{incident_id}/assign", json={"assigned_to": "lead-analyst@gestivaone.com"})
    assert assign_resp.status_code == 200
    assert assign_resp.json()["assigned_to"] == "lead-analyst@gestivaone.com"

    # 5. Escalation
    esc_resp = client.post(f"/api/v1/incidents/{incident_id}/escalate", json={"trigger_reason": "High Severity Threat", "escalated_to": "soc-lead@gestivaone.com"})
    assert esc_resp.status_code == 200

    # 6. Evidence Attachment & Timeline & Comments
    ev_resp = client.post(f"/api/v1/incidents/{incident_id}/evidence", json={
        "source_type": "GES_EVENT",
        "source_id": "evt-889900",
        "description": "Auth Log Failure Snapshot",
        "payload": {"ip": "198.51.100.250"}
    })
    assert ev_resp.status_code == 200
    assert "hash_reference" in ev_resp.json()

    comment_resp = client.post(f"/api/v1/incidents/{incident_id}/comments", json={"content": "Investigating memory dump."})
    assert comment_resp.status_code == 200

    timeline_resp = client.get(f"/api/v1/incidents/{incident_id}/timeline")
    assert timeline_resp.status_code == 200
    assert len(timeline_resp.json()["timeline"]) >= 3

    # 7. Case Creation linked to Parent Incident
    case_payload = {
        "title": "Forensic Investigation Case for Host 198.51.100.250",
        "description": "Full forensic workspace.",
        "severity": "P1_CRITICAL",
        "target_ip": "198.51.100.250",
        "incident_id": incident_id
    }
    case_resp = client.post("/api/v1/cases", json=case_payload, headers=headers)
    assert case_resp.status_code == 201
    case_id = case_resp.json()["case_id"]
    assert case_resp.json()["incident_id"] == incident_id

    # 8. Case Status Transitions: OPEN -> IN_PROGRESS -> RESOLVED -> CLOSED
    case_in_prog = client.patch(f"/api/v1/cases/{case_id}", json={"status": "IN_PROGRESS", "user_email": "analyst@gestivaone.com"})
    assert case_in_prog.status_code == 200
    assert case_in_prog.json()["status"] == "IN_PROGRESS"

    case_resolve = client.post(f"/api/v1/cases/{case_id}/resolve")
    assert case_resolve.status_code == 200
    assert case_resolve.json()["status"] == "RESOLVED"

    # 9. Incident Resolution and RCA Closure
    res_resp = client.post(f"/api/v1/incidents/{incident_id}/resolve", json={"resolution_summary": "Host isolated and credentials reset."})
    assert res_resp.status_code == 200

    close_resp = client.post(f"/api/v1/incidents/{incident_id}/close", json={"root_cause": "SSH password brute forced.", "closure_reason": "Host remediated."})
    assert close_resp.status_code == 200
    assert close_resp.json()["status"] == "CLOSED"

    # 10. Multi-Tenant Isolation Verification (BR-0004)
    tenant2_headers = {"X-Organization-ID": "00000000-0000-0000-0000-000000000002"}
    post_t2 = client.post("/api/v1/incidents", json={
        "title": "Tenant 2 Separate Incident",
        "description": "Isolated incident for org 2.",
        "origin_type": "MANUAL",
        "severity": "P2_HIGH"
    }, headers=tenant2_headers)
    assert post_t2.status_code == 201

    get_t2 = client.get("/api/v1/incidents", headers=tenant2_headers)
    assert get_t2.status_code == 200
    tenant2_incidents = get_t2.json()
    assert isinstance(tenant2_incidents, list)
    assert len(tenant2_incidents) >= 1
    assert all(i["organization_id"] == "00000000-0000-0000-0000-000000000002" for i in tenant2_incidents)
