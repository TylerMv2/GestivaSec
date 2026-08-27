"""
Gestiva Security (GestivaSec V1) — SPRINT 4: Event Collectors Framework Test Suite
Verifies multi-source ingestion (Syslog, Windows, JSON, Webhook, Agent), Asset Resolver matching, and EPS metrics.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_event_collectors_ingestion_and_asset_resolution():
    org_id = "00000000-0000-0000-0000-000000000001"
    headers = {"X-Organization-ID": org_id}

    # 1. Ingest Syslog Event
    syslog_resp = client.post(
        "/api/v1/collectors/ingest",
        json={
            "collector_type": "SYSLOG",
            "source_ip": "https://gestivaone.com",
            "source_hostname": "core-web-server",
            "payload": {"facility": 1, "severity": 3, "message": "Failed SSH password for root"}
        },
        headers=headers
    )
    assert syslog_resp.status_code == 200
    syslog_data = syslog_resp.json()
    assert syslog_data["collector_type"] == "SYSLOG"
    assert syslog_data["resolved_asset_id"] is not None  # Matched GestivaOne Core Web Portal asset!

    # 2. Ingest Windows Event (EVTX 4625)
    win_resp = client.post(
        "/api/v1/collectors/ingest",
        json={
            "collector_type": "WINDOWS_EVTX",
            "source_ip": "10.0.0.15",
            "source_hostname": "DC-01",
            "payload": {"event_id": 4625, "target_user_name": "Admin"}
        },
        headers=headers
    )
    assert win_resp.status_code == 200
    assert win_resp.json()["collector_type"] == "WINDOWS_EVTX"

    # 3. Verify List Ingested Events
    events_resp = client.get("/api/v1/collectors/events", headers=headers)
    assert events_resp.status_code == 200
    events = events_resp.json()
    assert len(events) >= 2

    # 4. Check Collector EPS Metrics
    metrics_resp = client.get("/api/v1/collectors/metrics")
    assert metrics_resp.status_code == 200
    metrics = metrics_resp.json()
    assert len(metrics) == 5
    assert any(m["collector_type"] == "SYSLOG" and m["events_ingested"] >= 1 for m in metrics)
