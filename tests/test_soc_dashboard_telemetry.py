"""
Gestiva Security (GestivaSec V1) — SOC Dashboard Telemetry API Test Suite
Verifies live polling telemetry widgets: Hosts Online, Critical Alerts, CPU/RAM, Traffic/min, TLS certs, and Active Sessions.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_get_soc_dashboard_telemetry_success():
    response = client.get(
        "/api/v1/soc/dashboard/telemetry",
        headers={"X-Organization-ID": "00000000-0000-0000-0000-000000000001"}
    )
    assert response.status_code == 200
    data = response.json()

    assert "hosts_online" in data
    assert "total_hosts" in data
    assert "critical_alerts_count" in data
    assert "traffic_mbps" in data
    assert "cpu_usage_pct" in data
    assert "ram_usage_pct" in data
    assert "events_per_minute" in data
    assert "expiring_tls_certs_count" in data
    assert "active_sessions_count" in data
    assert "traffic_labels" in data
    assert "traffic_data_mbps" in data
    assert len(data["traffic_labels"]) == 7
    assert len(data["traffic_data_mbps"]) == 7
    assert "services_status" in data
    assert len(data["services_status"]) >= 1
