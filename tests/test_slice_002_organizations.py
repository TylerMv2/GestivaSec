import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.domain.organization import Organization

client = TestClient(app)

def test_domain_organization_validation():
    """Validates organization name constraint."""
    with pytest.raises(ValueError, match="al menos 3 caracteres"):
        Organization(id=None, name="Ab", slug="ab")

def test_domain_organization_slug_generation():
    org = Organization(id=None, name="GestivaOne Cyber Division", slug="")
    assert org.slug == "gestivaone-cyber-division"

def test_rest_api_list_organizations():
    response = client.get("/api/v1/organizations")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert data[0]["slug"] == "gestivaone-corp"

def test_rest_api_create_organization():
    payload = { "name": "Global SOC Operations Center" }
    response = client.post("/api/v1/organizations", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Global SOC Operations Center"
    assert data["slug"] == "global-soc-operations-center"

def test_rest_api_get_current_organization():
    headers = { "X-Organization-ID": "00000000-0000-0000-0000-000000000001" }
    response = client.get("/api/v1/organizations/current", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "00000000-0000-0000-0000-000000000001"
    assert data["slug"] == "gestivaone-corp"
