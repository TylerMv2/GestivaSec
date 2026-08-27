import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_login_success():
    payload = {
        "email": "admin@gestivaone.com",
        "password": "GestivaSec2026!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["role"] == "SOC_ADMIN"
    assert data["email"] == "admin@gestivaone.com"

def test_login_invalid_password():
    payload = {
        "email": "admin@gestivaone.com",
        "password": "WrongPassword123!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401

def test_login_unknown_user():
    payload = {
        "email": "unknown@gestivaone.com",
        "password": "GestivaSec2026!"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 401

def test_get_current_user_authenticated():
    # 1. Login
    login_res = client.post("/api/v1/auth/login", json={
        "email": "admin@gestivaone.com",
        "password": "GestivaSec2026!"
    })
    token = login_res.json()["access_token"]

    # 2. Get profile
    response = client.get("/api/v1/auth/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "admin@gestivaone.com"
    assert data["role"] == "SOC_ADMIN"
