import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.infrastructure.passive_discovery_engine import PassiveDiscoveryEngine

client = TestClient(app)

def test_diagnostics_ping_endpoint():
    response = client.post("/diagnostics/ping", json={"target": "127.0.0.1"})
    assert response.status_code == 200
    data = response.json()
    assert "exit_code" in data
    assert data["exit_code"] == 0

def test_diagnostics_ping_invalid_input():
    response = client.post("/diagnostics/ping", json={"target": "127.0.0.1; rm -rf /"})
    assert response.status_code == 400

def test_diagnostics_dns_endpoint():
    response = client.post("/diagnostics/dns", json={"target": "localhost"})
    assert response.status_code == 200
    data = response.json()
    assert "stdout" in data

def test_diagnostics_terminal_command():
    response = client.post("/diagnostics/terminal", json={"command": "whoami"})
    assert response.status_code == 200
    data = response.json()
    assert data["exit_code"] == 0

def test_diagnostics_terminal_blocked_keyword():
    response = client.post("/diagnostics/terminal", json={"command": "rm -rf /"})
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_passive_discovery_engine_scan():
    report = await PassiveDiscoveryEngine.run_passive_scan("asset-100", "https://gestivaone.com")
    assert report.domain == "gestivaone.com"
    assert report.whois_record.registrar == "Cloudflare, Inc."
    assert "A" in report.dns_records
    assert report.headers_audit.grade in ["A+", "A", "B", "C", "D", "F"]
