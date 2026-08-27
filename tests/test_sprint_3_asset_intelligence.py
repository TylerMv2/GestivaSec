"""
Gestiva Security (GestivaSec V1) — SPRINT 3: Asset Intelligence & Lifecycle Test Suite
Verifies CMDB-grade Asset UUID, Exposure Risk Scoring, Lifecycle State Machine, and IP Forensic History.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from shared.constants import AssetStatus

client = TestClient(app)

def test_asset_intelligence_creation_and_risk_scoring():
    org_id = "00000000-0000-0000-0000-000000000001"
    headers = {"X-Organization-ID": org_id}

    # 1. Create Critical Asset
    resp = client.post(
        "/api/v1/assets",
        json={
            "name": "GestivaSec Payment Gateway",
            "target_url": "https://pay.gestivaone.com",
            "criticality": "P1_CRITICAL",
            "owner_email": "ciso@gestivaone.com",
            "department": "Fintech SOC Operations",
            "os_family": "RedHat Enterprise Linux 9"
        },
        headers=headers
    )
    assert resp.status_code == 201
    asset = resp.json()
    assert asset["id"] is not None
    assert asset["risk_score"] >= 50.0  # High risk base for P1 Critical
    assert asset["fingerprint_confidence"] == 0.95
    assert asset["department"] == "Fintech SOC Operations"

    asset_id = asset["id"]

    # 2. Lifecycle State Machine Transition (ACTIVE -> UNDER_MAINTENANCE)
    lc_resp = client.patch(
        f"/api/v1/assets/{asset_id}/lifecycle",
        json={"status": "UNDER_MAINTENANCE"},
        headers=headers
    )
    assert lc_resp.status_code == 200
    assert lc_resp.json()["status"] == "UNDER_MAINTENANCE"

    # 3. Location Update & Forensic IP History Log
    loc_resp = client.post(
        f"/api/v1/assets/{asset_id}/location",
        json={"new_target_url": "https://pay-v2.gestivaone.com"},
        headers=headers
    )
    assert loc_resp.status_code == 200
    updated_asset = loc_resp.json()
    assert updated_asset["target_url"] == "https://pay-v2.gestivaone.com"
    assert len(updated_asset["ip_history"]) == 1
    assert updated_asset["ip_history"][0]["ip_address"] == "https://pay.gestivaone.com"
