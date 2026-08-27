import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.domain.asset import DigitalAsset

client = TestClient(app)

def test_domain_asset_br02_owner_required():
    """BR-02: Every registered asset must have an assigned owner email."""
    with pytest.raises(ValueError, match="BR-02 Violation"):
        DigitalAsset(
            id=None,
            organization_id="00000000-0000-0000-0000-000000000001",
            name="Orphan Asset",
            target_url="https://orphan.org",
            criticality="P3_MEDIUM",
            owner_email="", # Invalid!
            status="REGISTERED"
        )

def test_domain_asset_br04_tenant_required():
    """BR-04: Organization boundary is required."""
    with pytest.raises(ValueError, match="BR-04 Violation"):
        DigitalAsset(
            id=None,
            organization_id="", # Invalid!
            name="No Tenant Asset",
            target_url="https://notenant.org",
            criticality="P3_MEDIUM",
            owner_email="valid@gestivaone.com",
            status="REGISTERED"
        )

def test_rest_api_list_assets():
    response = client.get("/api/v1/assets")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    assert data[0]["target_url"] == "https://gestivaone.com"

def test_rest_api_create_asset_success():
    payload = {
        "name": "GestivaOne Analytics Engine",
        "target_url": "https://analytics.gestivaone.com",
        "criticality": "P2_HIGH",
        "owner_email": "analytics-team@gestivaone.com"
    }
    response = client.post("/api/v1/assets", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "GestivaOne Analytics Engine"
    assert data["owner_email"] == "analytics-team@gestivaone.com"
    assert data["status"] == "ACTIVE"
