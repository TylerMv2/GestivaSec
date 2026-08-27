"""
Gestiva Security (GestivaSec V1) — SPRINT 5: Event Normalization Engine Test Suite
Verifies transformation of raw events into GestivaSec Event Schema (GES), GeoIP/ASN enrichment, and categorization.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_event_normalization_to_ges_schema():
    org_id = "00000000-0000-0000-0000-000000000001"
    headers = {"X-Organization-ID": org_id}

    # 1. Normalize Windows EVTX 4672 (Privilege Escalation)
    win_resp = client.post(
        "/api/v1/normalization/normalize",
        json={
            "collector_type": "WINDOWS_EVTX",
            "source_ip": "203.0.113.45",
            "source_hostname": "DC-01.gestivaone.internal",
            "payload": {"event_id": 4672, "target_user_name": "SYSTEM"}
        },
        headers=headers
    )
    assert win_resp.status_code == 200
    win_data = win_resp.json()
    
    # Check GestivaSec Event Schema (GES) fields
    assert win_data["event_id"] is not None
    assert win_data["source"]["ip"] == "203.0.113.45"
    assert win_data["source"]["geo_country"] == "US"
    assert win_data["source"]["geo_asn"] == "AS16509_AMAZON"
    assert win_data["event"]["category"] == "AUTHENTICATION"
    assert win_data["event"]["action"] == "PRIVILEGE_ESCALATION"
    assert win_data["event"]["severity"] == "CRITICAL"

    # 2. Normalize Syslog Auth Failure
    syslog_resp = client.post(
        "/api/v1/normalization/normalize",
        json={
            "collector_type": "SYSLOG",
            "source_ip": "192.168.1.50",
            "source_hostname": "web-node-01",
            "payload": {"message": "Failed password for invalid user root from 192.168.1.50 port 52102 ssh2"}
        },
        headers=headers
    )
    assert syslog_resp.status_code == 200
    syslog_data = syslog_resp.json()
    assert syslog_data["source"]["geo_country"] == "INT"
    assert syslog_data["event"]["action"] == "LOGIN_FAILED"

    # 3. List Normalized Events Log
    events_resp = client.get("/api/v1/normalization/events", headers=headers)
    assert events_resp.status_code == 200
    events = events_resp.json()
    assert len(events) >= 2
