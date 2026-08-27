"""
Gestiva Security (GestivaSec V1) — Comprehensive Passive Discovery REST API Router
Exposes /api/v1/passive endpoints for ASN, WHOIS, DNS, TLS, Headers, CDN, Tech Fingerprint & Changes.
"""
from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.application.passive_discovery_service import PassiveDiscoveryService
from backend.application.asset_service import AssetApplicationService

router = APIRouter(prefix="/api/v1/passive", tags=["Passive Security Discovery"])
passive_service = PassiveDiscoveryService()
asset_service = AssetApplicationService()

class AsnSchema(BaseModel):
    asn: str
    organization: str
    country: str
    ip_range: str

class WhoisSchema(BaseModel):
    registrar: str
    creation_date: str
    expiration_date: str
    name_servers: List[str]

class TechFingerprintSchema(BaseModel):
    web_server: str
    framework: str
    cdn: Optional[str]
    favicon_hash: str
    detected_technologies: List[str]

class TlsInfoSchema(BaseModel):
    subject: str
    issuer: str
    serial_number: str
    days_until_expiration: int
    is_valid: bool
    san_list: List[str]

class HeadersAuditSchema(BaseModel):
    hsts: bool
    content_security_policy: bool
    x_frame_options: bool
    x_content_type_options: bool
    referrer_policy: bool
    grade: str

class ChangeDeltaSchema(BaseModel):
    event_type: str
    description: str
    severity: str
    detected_at: str

class ComprehensivePassiveReportResponse(BaseModel):
    asset_id: str
    target_url: str
    domain: str
    resolved_ip: str
    asn_info: AsnSchema
    whois_record: WhoisSchema
    tech_fingerprint: TechFingerprintSchema
    dns_records: Dict[str, List[str]]
    tls_info: Optional[TlsInfoSchema]
    headers_audit: HeadersAuditSchema
    threat_score: int
    discovered_subdomains: List[str]
    detected_changes: List[ChangeDeltaSchema]
    scanned_at: str

@router.post("/scan/{asset_id}", response_model=ComprehensivePassiveReportResponse, status_code=status.HTTP_200_OK)
async def scan_asset_passively(asset_id: str):
    """Executes a comprehensive passive non-intrusive security discovery scan."""
    asset = await asset_service.get_asset(asset_id, "00000000-0000-0000-0000-000000000001")
    target_url = asset.target_url if asset else "https://gestivaone.com"

    report = await passive_service.scan_asset(asset_id, target_url)

    return ComprehensivePassiveReportResponse(
        asset_id=report.asset_id,
        target_url=report.target_url,
        domain=report.domain,
        resolved_ip=report.resolved_ip,
        asn_info=AsnSchema(
            asn=report.asn_info.asn,
            organization=report.asn_info.organization,
            country=report.asn_info.country,
            ip_range=report.asn_info.ip_range
        ),
        whois_record=WhoisSchema(
            registrar=report.whois_record.registrar,
            creation_date=report.whois_record.creation_date,
            expiration_date=report.whois_record.expiration_date,
            name_servers=report.whois_record.name_servers
        ),
        tech_fingerprint=TechFingerprintSchema(
            web_server=report.tech_fingerprint.web_server,
            framework=report.tech_fingerprint.framework,
            cdn=report.tech_fingerprint.cdn,
            favicon_hash=report.tech_fingerprint.favicon_hash,
            detected_technologies=report.tech_fingerprint.detected_technologies
        ),
        dns_records=report.dns_records,
        tls_info=TlsInfoSchema(
            subject=report.tls_info.subject,
            issuer=report.tls_info.issuer,
            serial_number=report.tls_info.serial_number,
            days_until_expiration=report.tls_info.days_until_expiration,
            is_valid=report.tls_info.is_valid,
            san_list=report.tls_info.san_list
        ) if report.tls_info else None,
        headers_audit=HeadersAuditSchema(
            hsts=report.headers_audit.hsts,
            content_security_policy=report.headers_audit.content_security_policy,
            x_frame_options=report.headers_audit.x_frame_options,
            x_content_type_options=report.headers_audit.x_content_type_options,
            referrer_policy=report.headers_audit.referrer_policy,
            grade=report.headers_audit.grade
        ),
        threat_score=report.threat_score,
        discovered_subdomains=report.discovered_subdomains,
        detected_changes=[
            ChangeDeltaSchema(
                event_type=c.event_type,
                description=c.description,
                severity=c.severity,
                detected_at=c.detected_at.isoformat()
            )
            for c in report.detected_changes
        ],
        scanned_at=report.scanned_at.isoformat()
    )

@router.get("/report/{asset_id}", response_model=ComprehensivePassiveReportResponse)
async def get_passive_report(asset_id: str):
    report = await passive_service.get_report(asset_id)
    if not report:
        return await scan_asset_passively(asset_id)

    return ComprehensivePassiveReportResponse(
        asset_id=report.asset_id,
        target_url=report.target_url,
        domain=report.domain,
        resolved_ip=report.resolved_ip,
        asn_info=AsnSchema(
            asn=report.asn_info.asn,
            organization=report.asn_info.organization,
            country=report.asn_info.country,
            ip_range=report.asn_info.ip_range
        ),
        whois_record=WhoisSchema(
            registrar=report.whois_record.registrar,
            creation_date=report.whois_record.creation_date,
            expiration_date=report.whois_record.expiration_date,
            name_servers=report.whois_record.name_servers
        ),
        tech_fingerprint=TechFingerprintSchema(
            web_server=report.tech_fingerprint.web_server,
            framework=report.tech_fingerprint.framework,
            cdn=report.tech_fingerprint.cdn,
            favicon_hash=report.tech_fingerprint.favicon_hash,
            detected_technologies=report.tech_fingerprint.detected_technologies
        ),
        dns_records=report.dns_records,
        tls_info=TlsInfoSchema(
            subject=report.tls_info.subject,
            issuer=report.tls_info.issuer,
            serial_number=report.tls_info.serial_number,
            days_until_expiration=report.tls_info.days_until_expiration,
            is_valid=report.tls_info.is_valid,
            san_list=report.tls_info.san_list
        ) if report.tls_info else None,
        headers_audit=HeadersAuditSchema(
            hsts=report.headers_audit.hsts,
            content_security_policy=report.headers_audit.content_security_policy,
            x_frame_options=report.headers_audit.x_frame_options,
            x_content_type_options=report.headers_audit.x_content_type_options,
            referrer_policy=report.headers_audit.referrer_policy,
            grade=report.headers_audit.grade
        ),
        threat_score=report.threat_score,
        discovered_subdomains=report.discovered_subdomains,
        detected_changes=[
            ChangeDeltaSchema(
                event_type=c.event_type,
                description=c.description,
                severity=c.severity,
                detected_at=c.detected_at.isoformat()
            )
            for c in report.detected_changes
        ],
        scanned_at=report.scanned_at.isoformat()
    )
