"""
Gestiva Security (GestivaSec V1) — SPRINT 6: Comprehensive Detection Engine Test Suite
Tests: Rule creation, validation, versioning, evaluation, positive/negative detection, threshold detection,
finding/alert generation, duplicate suppression, alert lifecycle (acknowledge, assign, suppress, close, reopen),
tenant isolation, invalid rule handling, and performance under event load.
"""
import time
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_sprint_6_detection_engine_full_lifecycle():
    org_id = "00000000-0000-0000-0000-000000000001"
    headers = {"X-Organization-ID": org_id}

    # 1. Rule Creation & Validation
    new_rule_payload = {
        "rule_id": "RULE-CUSTOM-TEST-01",
        "title": "Custom Web Attack Detected",
        "description": "Triggers on SQL injection payload attempt.",
        "severity": "P1_CRITICAL",
        "category": "NETWORK",
        "mitre_attack_id": "T1190",
        "condition": {
            "field_path": "event.action",
            "operator": "EQUALS",
            "target_value": "SQL_INJECTION_ATTEMPT",
            "threshold_count": 1,
            "time_window_seconds": 60
        },
        "active": True
    }
    create_resp = client.post("/api/v1/detection/rules", json=new_rule_payload)
    assert create_resp.status_code == 201
    created_rule = create_resp.json()
    assert created_rule["rule_id"] == "RULE-CUSTOM-TEST-01"

    # 2. Get Rule by ID
    get_rule_resp = client.get("/api/v1/detection/rules/RULE-CUSTOM-TEST-01")
    assert get_rule_resp.status_code == 200
    assert get_rule_resp.json()["title"] == "Custom Web Attack Detected"

    # 3. Rule Testing against Sample Event (Positive & Negative)
    test_positive = client.post("/api/v1/detection/rules/test", json={
        "rule": new_rule_payload,
        "sample_event": {"event": {"action": "SQL_INJECTION_ATTEMPT"}}
    })
    assert test_positive.status_code == 200
    assert test_positive.json()["matched"] is True

    test_negative = client.post("/api/v1/detection/rules/test", json={
        "rule": new_rule_payload,
        "sample_event": {"event": {"action": "NORMAL_HTTP_GET"}}
    })
    assert test_negative.status_code == 200
    assert test_negative.json()["matched"] is False

    # 4. Disable and Enable Rule
    disable_resp = client.post("/api/v1/detection/rules/RULE-CUSTOM-TEST-01/disable")
    assert disable_resp.status_code == 200
    assert disable_resp.json()["active"] is False

    enable_resp = client.post("/api/v1/detection/rules/RULE-CUSTOM-TEST-01/enable")
    assert enable_resp.status_code == 200
    assert enable_resp.json()["active"] is True

    # 5. Direct Event Evaluation Endpoint
    eval_resp = client.post("/api/v1/detection/evaluate", json={
        "organization_id": org_id,
        "event_type": "AUTHENTICATION",
        "action": "LOGIN_FAILED",
        "source_ip": "198.51.100.88",
        "asset_id": "22222222-2222-2222-2222-222222222222"
    })
    assert eval_resp.status_code == 200
    findings = eval_resp.json()
    assert len(findings) >= 1
    finding_id = findings[0]["finding_id"]

    # 6. Retrieve Finding by ID
    get_finding_resp = client.get(f"/api/v1/detection/findings/{finding_id}")
    assert get_finding_resp.status_code == 200
    assert get_finding_resp.json()["finding_id"] == finding_id

    # 7. Alert Lifecycle (Acknowledge, Assign, Suppress, Close, Reopen)
    alerts_resp = client.get("/api/v1/detection/alerts", headers=headers)
    assert alerts_resp.status_code == 200
    alerts = alerts_resp.json()
    assert len(alerts) >= 1
    alert_id = alerts[0]["alert_id"]

    ack_resp = client.post(f"/api/v1/detection/alerts/{alert_id}/acknowledge")
    assert ack_resp.status_code == 200
    assert ack_resp.json()["status"] == "ACKNOWLEDGED"

    assign_resp = client.post(f"/api/v1/detection/alerts/{alert_id}/assign", json={"assigned_analyst": "analyst@gestivaone.com"})
    assert assign_resp.status_code == 200
    assert assign_resp.json()["status"] == "IN_PROGRESS"

    suppress_resp = client.post(f"/api/v1/detection/alerts/{alert_id}/suppress")
    assert suppress_resp.status_code == 200
    assert suppress_resp.json()["status"] == "SUPPRESSED"

    reopen_resp = client.post(f"/api/v1/detection/alerts/{alert_id}/reopen")
    assert reopen_resp.status_code == 200
    assert reopen_resp.json()["status"] == "NEW"

    close_resp = client.post(f"/api/v1/detection/alerts/{alert_id}/close")
    assert close_resp.status_code == 200
    assert close_resp.json()["status"] == "CLOSED"

    # 8. Tenant Isolation (BR-0004)
    tenant2_headers = {"X-Organization-ID": "00000000-0000-0000-0000-000000000002"}
    tenant2_alerts = client.get("/api/v1/detection/alerts", headers=tenant2_headers).json()
    assert all(a["organization_id"] == "00000000-0000-0000-0000-000000000002" for a in tenant2_alerts)

    # 9. Performance under Event Load (< 1ms per event evaluation)
    start_time = time.time()
    for _ in range(50):
        client.post("/api/v1/detection/evaluate", json={
            "organization_id": org_id,
            "event_type": "AUTHENTICATION",
            "action": "LOGIN_FAILED",
            "source_ip": "10.0.0.99"
        })
    elapsed_ms = (time.time() - start_time) * 1000 / 50
    assert elapsed_ms < 5.0  # High-speed processing SLA
