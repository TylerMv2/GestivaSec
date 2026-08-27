"""
Gestiva Security (GestivaSec V1) — SLICE-007: Session Management & Invalidation Test Suite
Verifies Session Tracking, JWT Logout, and Token Invalidation Blacklist (BR-0005).
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.domain.session import clear_blacklist, is_token_revoked

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_teardown_blacklist():
    clear_blacklist()
    yield
    clear_blacklist()

def test_login_and_logout_flow_success():
    # 1. Login
    login_resp = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@gestivaone.com", "password": "GestivaSec2026!"}
    )
    assert login_resp.status_code == 200
    token = login_resp.json()["access_token"]
    assert token is not None

    # 2. Verify /me works before logout
    headers = {"Authorization": f"Bearer {token}"}
    me_resp = client.get("/api/v1/auth/me", headers=headers)
    assert me_resp.status_code == 200
    assert me_resp.json()["email"] == "admin@gestivaone.com"

    # 3. Logout
    logout_resp = client.post("/api/v1/auth/logout", headers=headers)
    assert logout_resp.status_code == 200
    assert logout_resp.json()["message"] == "Sesión cerrada exitosamente y token revocado."

    # 4. Verify token is in blacklist
    assert is_token_revoked(token) is True

    # 5. Verify /me fails with 401 after logout
    me_after_logout = client.get("/api/v1/auth/me", headers=headers)
    assert me_after_logout.status_code == 401
    assert "inválido" in me_after_logout.json()["detail"].lower() or "invalidado" in me_after_logout.json()["detail"].lower()

def test_logout_without_token_fails():
    resp = client.post("/api/v1/auth/logout")
    assert resp.status_code == 401
