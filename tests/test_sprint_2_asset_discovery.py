"""
Gestiva Security (GestivaSec V1) — SPRINT 2: Asset Discovery Test Suite
Verifies automated network scanning, port probing, OS fingerprinting, and asset promotion.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_execute_network_discovery_scan():
    org_id = "00000000-0000-0000-0000-000000000001"
    headers = {"X-Organization-ID": org_id}
    
    # 1. Trigger scan
    scan_resp = client.post(
        "/api/v1/discovery/scan",
        json={"target_cidr": "127.0.0.1/32"},
        headers=headers
    )
    assert scan_resp.status_code == 200
    scan_data = scan_resp.json()
    assert scan_data["status"] == "COMPLETED"
    assert scan_data["total_hosts_found"] >= 1
    assert scan_data["hosts"][0]["ip_address"] == "127.0.0.1"
    assert len(scan_data["hosts"][0]["open_ports"]) >= 1

    host_id = scan_data["hosts"][0]["host_id"]

    # 2. List Discovered Hosts
    list_resp = client.get("/api/v1/discovery/hosts", headers=headers)
    assert list_resp.status_code == 200
    hosts = list_resp.json()
    assert any(h["host_id"] == host_id for h in hosts)

    # 3. Promote Host to Asset
    promote_resp = client.post(
        "/api/v1/discovery/promote",
        json={"host_id": host_id, "owner_email": "secops@gestivaone.com"},
        headers=headers
    )
    assert promote_resp.status_code == 200
    promote_data = promote_resp.json()
    assert promote_data["status"] == "PROMOTED"
    assert "asset_id" in promote_data
