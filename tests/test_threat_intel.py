import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.domain.threat_intel import (
    ThreatIntelReport,
    VirusTotalIndicator,
    AbuseIpDbIndicator,
    GreyNoiseIndicator,
    CisaKevIndicator,
    NvdCveIndicator
)

client = TestClient(app)

def test_domain_threat_score_calculation():
    vt = VirusTotalIndicator(malicious_votes=2, suspicious_votes=1, reputation=50, last_analysis_date="2026-07-25")
    abuse = AbuseIpDbIndicator(abuse_confidence_score=50, total_reports=10, is_whitelisted=False, last_reported_at="2026-07-25")
    greynoise = GreyNoiseIndicator(is_noise=False, is_malicious=True, actor="BadActor", tags=["scanner"])
    cisa = CisaKevIndicator(is_known_exploited=True, cve_id="CVE-2024-3094", vulnerability_name="XZ Utils RCE", action_due_date="2026-08-01")
    nvd = [NvdCveIndicator(cve_id="CVE-2024-3094", cvss_v3_score=10.0, severity="CRITICAL")]

    report = ThreatIntelReport(
        asset_id="test-asset",
        domain="gestivaone.com",
        resolved_ip="104.21.55.12",
        virustotal=vt,
        abuseipdb=abuse,
        greynoise=greynoise,
        cisa_kev=cisa,
        nvd_cves=nvd,
        composite_threat_score=0,
        threat_grade="CRITICAL"
    )
    score = report.calculate_threat_score()
    assert score == 100  # Capped at 100

def test_rest_api_threat_intel_enrichment():
    assets_res = client.get("/api/v1/assets")
    asset_id = assets_res.json()[0]["id"]

    response = client.post(f"/api/v1/threat-intel/enrich/{asset_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["asset_id"] == asset_id
    assert "virustotal" in data
    assert "abuseipdb" in data
    assert "greynoise" in data
    assert "cisa_kev" in data
    assert "composite_threat_score" in data
    assert "cached" in data

def test_rest_api_threat_intel_caching():
    assets_res = client.get("/api/v1/assets")
    asset_id = assets_res.json()[0]["id"]

    # First request -> Fresh
    res1 = client.post(f"/api/v1/threat-intel/enrich/{asset_id}")
    assert res1.status_code == 200
    
    # Second request -> Cached
    res2 = client.post(f"/api/v1/threat-intel/enrich/{asset_id}")
    assert res2.status_code == 200
    assert res2.json()["cached"] is True
