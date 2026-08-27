import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.infrastructure.passive_discovery_engine import PassiveDiscoveryEngine

client = TestClient(app)

def test_extract_domain():
    assert PassiveDiscoveryEngine.extract_domain("https://gestivaone.com/path") == "gestivaone.com"

@pytest.mark.asyncio
async def test_inspect_tls():
    tls_info = await PassiveDiscoveryEngine.inspect_tls("gestivaone.com")
    assert tls_info is not None
    assert tls_info.is_valid is True
    assert tls_info.days_until_expiration > 0

@pytest.mark.asyncio
async def test_audit_security_headers():
    audit, tech = await PassiveDiscoveryEngine.audit_security_headers_and_tech("https://gestivaone.com")
    assert audit.grade in ["A+", "A", "B", "C", "D", "F"]
    assert tech.cdn == "Cloudflare CDN"
    assert "FastAPI" in tech.framework

def test_rest_api_comprehensive_passive_scan():
    assets_res = client.get("/api/v1/assets")
    asset_id = assets_res.json()[0]["id"]

    response = client.post(f"/api/v1/passive/scan/{asset_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["asset_id"] == asset_id
    assert data["asn_info"]["asn"] == "AS13335"
    assert data["whois_record"]["registrar"] == "Cloudflare, Inc."
    assert data["tech_fingerprint"]["cdn"] == "Cloudflare CDN"
    assert "detected_changes" in data
    assert len(data["detected_changes"]) >= 1
