import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.domain.user import User

client = TestClient(app)

def test_domain_user_invalid_role():
    """Validates role assignment constraint."""
    with pytest.raises(ValueError, match="Rol 'INVALID_ROLE' inválido"):
        User(
            id=None,
            organization_id="00000000-0000-0000-0000-000000000001",
            email="test@gestivaone.com",
            password_hash="hash",
            role="INVALID_ROLE"
        )

def test_domain_user_br04_tenant_required():
    with pytest.raises(ValueError, match="BR-04 Violation"):
        User(
            id=None,
            organization_id="",
            email="test@gestivaone.com",
            password_hash="hash",
            role="SOC_ANALYST"
        )

def test_rest_api_list_users():
    response = client.get("/api/v1/users")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["email"] == "admin@gestivaone.com"

def test_rest_api_create_user():
    payload = {
        "email": "analyst.tier1@gestivaone.com",
        "password": "AnalystSec2026!",
        "role": "SOC_ANALYST"
    }
    response = client.post("/api/v1/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "analyst.tier1@gestivaone.com"
    assert data["role"] == "SOC_ANALYST"
    assert data["is_active"] is True
