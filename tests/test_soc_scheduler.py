import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_rest_api_list_scheduled_jobs():
    response = client.get("/api/v1/soc/scheduler/jobs")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 3
    job_types = [j["job_type"] for j in data]
    assert "1M_HTTP_HTTPS_LATENCY" in job_types
    assert "5M_DNS_MX_TXT_SPF_DKIM_DMARC" in job_types
    assert "1H_TLS_CIPHER_SAN" in job_types

def test_rest_api_trigger_1m_http_job():
    response = client.post("/api/v1/soc/scheduler/trigger/job-1m-http")
    assert response.status_code == 200
    data = response.json()
    assert data["job_id"] == "job-1m-http"
    assert data["status"] == "SUCCESS"
    assert "latency_ms" in data["details"]

def test_rest_api_trigger_5m_dns_job():
    response = client.post("/api/v1/soc/scheduler/trigger/job-5m-dns")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["details"]["has_spf"] is True

def test_rest_api_trigger_1h_tls_job():
    response = client.post("/api/v1/soc/scheduler/trigger/job-1h-tls")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "SUCCESS"
    assert data["details"]["tls_version"] == "TLSv1.3"

def test_rest_api_get_detected_changes():
    response = client.get("/api/v1/soc/scheduler/changes")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
