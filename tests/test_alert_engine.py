import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.domain.alert_engine import IncidentStatus

client = TestClient(app)

def test_rest_api_list_alerts():
    response = client.get("/api/v1/alerts")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["severity"] == "CRITICAL"

def test_rest_api_list_timeline():
    response = client.get("/api/v1/timeline")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["event_type"] == "ALERT"

def test_rest_api_list_incidents():
    response = client.get("/api/v1/incidents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["status"] == "INVESTIGATING"

def test_rest_api_transition_incident_success():
    response = client.post("/api/v1/incidents/inc-001/transition", json={
        "status": "CLOSED_WITH_RCA",
        "rca_report": "Root Cause Analysis: Event loop timeout resolved by scaling worker pool."
    })
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "CLOSED_WITH_RCA"
    assert "Root Cause Analysis" in data["rca_report"]

def test_rest_api_transition_incident_br01_violation():
    response = client.post("/api/v1/incidents/inc-001/transition", json={
        "status": "CLOSED_WITH_RCA"
    })
    assert response.status_code == 400
    assert "Regla BR-0001" in response.json()["detail"]
