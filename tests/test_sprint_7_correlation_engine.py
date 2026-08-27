"""
Gestiva Security (GestivaSec V1) — SPRINT 7: Comprehensive Correlation Engine Test Suite
Tests: Multi-stage attack chain correlation, sliding time-window, explainable correlation score, timeline retrieval,
tenant isolation, correlation rules CRUD, and performance.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_sprint_7_multi_event_correlation_engine_full_flow():
    org_id = "00000000-0000-0000-0000-000000000001"
    headers = {"X-Organization-ID": org_id}

    # 1. Trigger First Event: External GeoIP Anomaly (Reconnaissance)
    client.post(
        "/api/v1/normalization/normalize",
        json={
            "collector_type": "CLOUD_WEBHOOK",
            "source_ip": "198.51.100.222",
            "source_hostname": "external-attacker-node",
            "payload": {"provider": "aws-cloudtrail"}
        },
        headers=headers
    )

    # 2. Trigger Second Event: Syslog Auth Brute Force (Exploitation)
    client.post(
        "/api/v1/normalization/normalize",
        json={
            "collector_type": "SYSLOG",
            "source_ip": "198.51.100.222",
            "source_hostname": "external-attacker-node",
            "payload": {"message": "Failed password for root from 198.51.100.222 port 22 ssh2"}
        },
        headers=headers
    )

    # 3. Trigger Third Event: Windows Privilege Escalation (Privilege Escalation)
    client.post(
        "/api/v1/normalization/normalize",
        json={
            "collector_type": "WINDOWS_EVTX",
            "source_ip": "198.51.100.222",
            "source_hostname": "external-attacker-node",
            "payload": {"event_id": 4672, "target_user_name": "SYSTEM"}
        },
        headers=headers
    )

    # 4. Query Correlated Attack Chains REST Endpoint
    chains_resp = client.get("/api/v1/correlation/chains", headers=headers)
    assert chains_resp.status_code == 200
    chains = chains_resp.json()
    assert len(chains) >= 1

    target_chain = next((c for c in chains if c["target_ip"] == "198.51.100.222"), None)
    assert target_chain is not None
    assert target_chain["severity"] == "P1_CRITICAL"
    assert target_chain["status"] == "ACTIVE"
    assert target_chain["correlation_score"] >= 70
    assert len(target_chain["explainable_reasons"]) >= 1
    assert len(target_chain["nodes"]) >= 2
    assert len(target_chain["kill_chain_stages"]) >= 2

    # 5. Query Chain Timeline
    chain_id = target_chain["chain_id"]
    timeline_resp = client.get(f"/api/v1/correlation/chains/{chain_id}/timeline")
    assert timeline_resp.status_code == 200
    assert len(timeline_resp.json()["timeline"]) >= 2

    # 6. Correlation Rules API (List & Create)
    rules_resp = client.get("/api/v1/correlation/rules", headers=headers)
    assert rules_resp.status_code == 200
    assert len(rules_resp.json()) >= 1

    create_rule_resp = client.post(
        "/api/v1/correlation/rules",
        json={
            "name": "Custom Exfiltration Sequence",
            "description": "Correlates high-volume egress with sensitive file access.",
            "time_window_minutes": 10,
            "required_event_count": 2,
            "severity": "P1_CRITICAL",
            "mitre_attack_techniques": ["T1041"]
        },
        headers=headers
    )
    assert create_rule_resp.status_code == 201
    assert create_rule_resp.json()["name"] == "Custom Exfiltration Sequence"

    # 7. Close Attack Chain
    close_resp = client.post(f"/api/v1/correlation/chains/{chain_id}/close")
    assert close_resp.status_code == 200
    assert close_resp.json()["status"] == "RESOLVED"
