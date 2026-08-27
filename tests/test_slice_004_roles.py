import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.domain.role import RoleMatrix

client = TestClient(app)

def test_domain_role_matrix_lookup():
    admin = RoleMatrix.get_role("SOC_ADMIN")
    assert admin.name == "SOC_ADMIN"
    assert "*" in admin.permissions

def test_domain_role_invalid():
    with pytest.raises(ValueError, match="no existe en la Matriz RBAC"):
        RoleMatrix.get_role("NON_EXISTENT")

def test_rest_api_list_roles():
    response = client.get("/api/v1/roles")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 4
    role_names = [r["name"] for r in data]
    assert "SOC_ADMIN" in role_names
    assert "SOC_ANALYST" in role_names

def test_rest_api_get_specific_role():
    response = client.get("/api/v1/roles/SOC_ANALYST")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "SOC_ANALYST"
    assert "assets:read" in data["permissions"]
