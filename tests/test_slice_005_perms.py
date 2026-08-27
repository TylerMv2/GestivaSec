import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.domain.permission import PermissionEvaluator

client = TestClient(app)

def test_domain_permission_evaluator_admin_wildcard():
    assert PermissionEvaluator.is_authorized("SOC_ADMIN", "any:action") is True

def test_domain_permission_evaluator_analyst_permissions():
    assert PermissionEvaluator.is_authorized("SOC_ANALYST", "assets:read") is True
    assert PermissionEvaluator.is_authorized("SOC_ANALYST", "admin:delete_tenant") is False

def test_rest_api_check_permission_granted():
    response = client.get("/api/v1/permissions/check?role=SOC_ANALYST&permission=assets:read")
    assert response.status_code == 200
    data = response.json()
    assert data["is_authorized"] is True

def test_rest_api_check_permission_denied():
    response = client.get("/api/v1/permissions/check?role=SOC_OPERATOR&permission=incidents:delete")
    assert response.status_code == 200
    data = response.json()
    assert data["is_authorized"] is False

def test_rest_api_get_role_permissions():
    response = client.get("/api/v1/permissions/SOC_ANALYST")
    assert response.status_code == 200
    data = response.json()
    assert "assets:read" in data["permissions"]
