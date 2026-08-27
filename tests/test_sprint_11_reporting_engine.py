"""
Gestiva Security (GestivaSec V1) — STAGE 11: Enterprise Reporting Engine & Audit Export Test Suite
Tests: Report Templates, PDF/CSV/JSON Report Generation, Downloads, Audit Log Export, Tenant Isolation, and Audit Trail.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_sprint_11_enterprise_reporting_and_audit_export():
    org_id = "00000000-0000-0000-0000-000000000001"
    headers = {"X-Organization-ID": org_id}

    # 1. Query Report Templates
    tmpl_resp = client.get("/api/v1/reports/templates")
    assert tmpl_resp.status_code == 200
    templates = tmpl_resp.json()
    assert len(templates) >= 4
    assert any(t["template_id"] == "TMPL-EXEC-01" for t in templates)

    # 2. Generate Executive PDF Security Report
    gen_pdf_payload = {
        "template_id": "TMPL-EXEC-01",
        "title": "Q3 Executive Security Summary",
        "format": "PDF",
        "parameters": {"additional_note": "Quarterly Audit Passed"}
    }
    pdf_resp = client.post("/api/v1/reports/generate", json=gen_pdf_payload, headers=headers)
    assert pdf_resp.status_code == 201
    job_data = pdf_resp.json()
    job_id = job_data["job_id"]
    assert job_data["format"] == "PDF"
    assert job_data["status"] == "COMPLETED"

    # 3. Generate SOC Metrics CSV Report
    gen_csv_payload = {
        "template_id": "TMPL-METRICS-02",
        "format": "CSV"
    }
    csv_resp = client.post("/api/v1/reports/generate", json=gen_csv_payload, headers=headers)
    assert csv_resp.status_code == 201
    assert csv_resp.json()["format"] == "CSV"

    # 4. List Report Jobs for Tenant
    jobs_resp = client.get("/api/v1/reports/jobs", headers=headers)
    assert jobs_resp.status_code == 200
    jobs = jobs_resp.json()
    assert len(jobs) >= 2

    # 5. Download Report Content
    download_resp = client.get(f"/api/v1/reports/jobs/{job_id}/download")
    assert download_resp.status_code == 200
    assert "GESTIVA SECURITY ENTERPRISE SOC PLATFORM" in download_resp.text

    # 6. Export Compliance Audit Logs (CSV format)
    audit_exp_resp = client.post("/api/v1/reports/audit/export", json={"format": "CSV"}, headers=headers)
    assert audit_exp_resp.status_code == 201
    exp_data = audit_exp_resp.json()
    assert exp_data["status"] == "COMPLETED"

    # 7. Verify Tenant Isolation Boundary
    t2_headers = {"X-Organization-ID": "00000000-0000-0000-0000-000000000002"}
    t2_jobs = client.get("/api/v1/reports/jobs", headers=t2_headers).json()
    assert all(j["organization_id"] == "00000000-0000-0000-0000-000000000002" for j in t2_jobs)
