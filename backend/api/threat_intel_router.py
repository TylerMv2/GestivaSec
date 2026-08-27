"""
Gestiva Security (GestivaSec V1) — Threat Intelligence REST API Router
Exposes /api/v1/threat-intel endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.application.threat_intel_service import ThreatIntelApplicationService
from backend.application.asset_service import AssetApplicationService

router = APIRouter(prefix="/api/v1/threat-intel", tags=["Threat Intelligence Engine"])
intel_service = ThreatIntelApplicationService()
asset_service = AssetApplicationService()

class VirusTotalSchema(BaseModel):
    malicious_votes: int
    suspicious_votes: int
    reputation: int
    last_analysis_date: str

class AbuseIpDbSchema(BaseModel):
    abuse_confidence_score: int
    total_reports: int
    is_whitelisted: bool
    last_reported_at: str

class GreyNoiseSchema(BaseModel):
    is_noise: bool
    is_malicious: bool
    actor: str
    tags: List[str]

class CisaKevSchema(BaseModel):
    is_known_exploited: bool
    cve_id: Optional[str]
    vulnerability_name: Optional[str]
    action_due_date: Optional[str]

class NvdCveSchema(BaseModel):
    cve_id: str
    cvss_v3_score: float
    severity: str

class ThreatIntelReportResponse(BaseModel):
    asset_id: str
    domain: str
    resolved_ip: str
    virustotal: VirusTotalSchema
    abuseipdb: AbuseIpDbSchema
    greynoise: GreyNoiseSchema
    cisa_kev: CisaKevSchema
    nvd_cves: List[NvdCveSchema]
    composite_threat_score: int
    threat_grade: str
    cached: bool
    updated_at: str

@router.post("/enrich/{asset_id}", response_model=ThreatIntelReportResponse, status_code=status.HTTP_200_OK)
async def enrich_asset_threat_intel(asset_id: str):
    """Enriches asset with VirusTotal, AbuseIPDB, GreyNoise, CISA KEV, and NVD threat indicators."""
    asset = await asset_service.get_asset(asset_id, "00000000-0000-0000-0000-000000000001")
    domain = asset.target_url.replace("https://", "").replace("http://", "").split("/")[0] if asset else "gestivaone.com"

    report = await intel_service.enrich_asset(asset_id, domain, "104.21.55.12")

    return ThreatIntelReportResponse(
        asset_id=report.asset_id,
        domain=report.domain,
        resolved_ip=report.resolved_ip,
        virustotal=VirusTotalSchema(
            malicious_votes=report.virustotal.malicious_votes,
            suspicious_votes=report.virustotal.suspicious_votes,
            reputation=report.virustotal.reputation,
            last_analysis_date=report.virustotal.last_analysis_date
        ),
        abuseipdb=AbuseIpDbSchema(
            abuse_confidence_score=report.abuseipdb.abuse_confidence_score,
            total_reports=report.abuseipdb.total_reports,
            is_whitelisted=report.abuseipdb.is_whitelisted,
            last_reported_at=report.abuseipdb.last_reported_at
        ),
        greynoise=GreyNoiseSchema(
            is_noise=report.greynoise.is_noise,
            is_malicious=report.greynoise.is_malicious,
            actor=report.greynoise.actor,
            tags=report.greynoise.tags
        ),
        cisa_kev=CisaKevSchema(
            is_known_exploited=report.cisa_kev.is_known_exploited,
            cve_id=report.cisa_kev.cve_id,
            vulnerability_name=report.cisa_kev.vulnerability_name,
            action_due_date=report.cisa_kev.action_due_date
        ),
        nvd_cves=[
            NvdCveSchema(cve_id=c.cve_id, cvss_v3_score=c.cvss_v3_score, severity=c.severity)
            for c in report.nvd_cves
        ],
        composite_threat_score=report.composite_threat_score,
        threat_grade=report.threat_grade,
        cached=report.cached,
        updated_at=report.updated_at.isoformat()
    )
