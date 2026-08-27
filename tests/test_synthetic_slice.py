import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_rest_api_probe_existing_asset():
    # First get valid asset id
    assets_res = client.get("/api/v1/assets")
    assert assets_res.status_code == 200
    assets = assets_res.json()
    assert len(assets) > 0
    asset_id = assets[0]["id"]

    # Execute synthetic evaluation via REST endpoint
    response = client.post(f"/api/v1/probing/evaluate/{asset_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["asset_id"] == asset_id
    assert "latency_ms" in data
    assert "status_code" in data
    assert "is_successful" in data

def test_rest_api_probe_non_existent_asset():
    response = client.post("/api/v1/probing/evaluate/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 200
    data = response.json()
    assert data["asset_id"] == "00000000-0000-0000-0000-000000000000"
    assert data["status_code"] == 200
    assert data["latency_ms"] == 0.0
    assert data["is_successful"] is True

def test_rest_api_list_evaluations():
    response = client.get("/api/v1/probing/evaluations")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_rest_api_synthetic_and_audit_aliases():
    # Test /api/v1/synthetic/probe alias
    syn_res = client.post("/api/v1/synthetic/probe", json={"asset_id": "test-asset-cold"})
    assert syn_res.status_code == 200
    syn_data = syn_res.json()
    assert syn_data["asset_id"] == "test-asset-cold"

    # Test /api/v1/synthetic/probes alias
    syn_probes_res = client.get("/api/v1/synthetic/probes")
    assert syn_probes_res.status_code == 200
    assert isinstance(syn_probes_res.json(), list)

    # Test /api/v1/audit route (unauthenticated should return 401, not 404!)
    audit_res = client.get("/api/v1/audit")
    assert audit_res.status_code == 401
