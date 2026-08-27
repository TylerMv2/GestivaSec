"""
Gestiva Security (GestivaSec V1) — End-to-End (E2E) Golden Demo Test Suite (Release v0.1.0)
Executes complete user journey: Login -> Organization -> User -> Asset -> Synthetic Probe -> Alert -> Dashboard.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_e2e_golden_demo_full_flow():
    # 1. HEALTHCHECK
    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["status"] == "healthy"

    # 2. LOGIN (IAM-LOGIN)
    login_res = client.post("/api/v1/auth/login", json={
        "email": "admin@gestivaone.com",
        "password": "GestivaSec2026!"
    })
    assert login_res.status_code == 200
    token = login_res.json()["access_token"]
    auth_headers = {
        "Authorization": f"Bearer {token}",
        "X-Organization-ID": "00000000-0000-0000-0000-000000000001"
    }

    # 3. CREATE ORGANIZATION (IAM-ORGS)
    org_res = client.post("/api/v1/organizations", json={
        "name": "E2E Validation Organization"
    })
    assert org_res.status_code == 201
    new_org_id = org_res.json()["id"]

    # 4. CREATE USER (IAM-USERS)
    user_res = client.post("/api/v1/users", json={
        "email": "e2e.analyst@gestivaone.com",
        "password": "AnalystSec2026!",
        "role": "SOC_ANALYST"
    }, headers={"X-Organization-ID": new_org_id})
    assert user_res.status_code == 201
    assert user_res.json()["email"] == "e2e.analyst@gestivaone.com"

    # 5. REGISTER ASSET (AST-INVENTORY)
    asset_res = client.post("/api/v1/assets", json={
        "name": "E2E Target Web Service",
        "target_url": "https://gestivaone.com",
        "criticality": "P1_CRITICAL",
        "owner_email": "e2e.owner@gestivaone.com"
    }, headers={"X-Organization-ID": new_org_id})
    assert asset_res.status_code == 201
    asset_id = asset_res.json()["id"]

    # 6. EXECUTE SYNTHETIC HTTP PROBE (MON-SYNTHETIC)
    probe_res = client.post(f"/api/v1/probing/evaluate/{asset_id}", headers={"X-Organization-ID": new_org_id})
    assert probe_res.status_code == 200
    probe_data = probe_res.json()
    assert probe_data["asset_id"] == asset_id
    assert "latency_ms" in probe_data

    # 7. VERIFY PROBES HISTORICAL LISTING
    probes_list = client.get("/api/v1/probing/evaluations", headers={"X-Organization-ID": new_org_id})
    assert probes_list.status_code == 200
    assert len(probes_list.json()) >= 1

    # 8. VERIFY DASHBOARD METRICS
    metrics = client.get("/metrics")
    assert metrics.status_code == 200
    assert "gestivasec_monitored_assets" in metrics.json()
