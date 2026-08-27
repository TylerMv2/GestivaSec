"""
Gestiva Security (GestivaSec V1) — Comprehensive Passive Discovery & Change Detection Domain Model
Encapsulates DNS, Subdomains, ASN, WHOIS, TLS, Headers, CDN, Tech Fingerprint, and Historical Change Deltas.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime

@dataclass
class AsnInfo:
    asn: str
    organization: str
    country: str
    ip_range: str

@dataclass
class WhoisRecord:
    registrar: str
    creation_date: str
    expiration_date: str
    name_servers: List[str]

@dataclass
class TechnologyFingerprint:
    web_server: str
    framework: str
    cdn: Optional[str]
    favicon_hash: str
    detected_technologies: List[str]

@dataclass
class TlsCertificateInfo:
    subject: str
    issuer: str
    serial_number: str
    valid_from: datetime
    valid_to: datetime
    days_until_expiration: int
    is_valid: bool
    san_list: List[str] = field(default_factory=list)

@dataclass
class SecurityHeadersAudit:
    hsts: bool
    content_security_policy: bool
    x_frame_options: bool
    x_content_type_options: bool
    referrer_policy: bool
    grade: str

    def calculate_grade(self) -> str:
        score = sum([self.hsts, self.content_security_policy, self.x_frame_options, self.x_content_type_options, self.referrer_policy])
        if score == 5: return "A+"
        elif score == 4: return "A"
        elif score == 3: return "B"
        elif score == 2: return "C"
        else: return "F"

@dataclass
class ChangeDelta:
    event_type: str  # "NEW_SUBDOMAIN", "IP_CHANGED", "TLS_RENEWED", "HEADER_REMOVED"
    description: str
    severity: str  # "INFO", "LOW", "MEDIUM", "HIGH", "CRITICAL"
    detected_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class PassiveDiscoveryReport:
    asset_id: str
    target_url: str
    domain: str
    resolved_ip: str
    asn_info: AsnInfo
    whois_record: WhoisRecord
    tech_fingerprint: TechnologyFingerprint
    dns_records: Dict[str, List[str]]
    tls_info: Optional[TlsCertificateInfo]
    headers_audit: SecurityHeadersAudit
    threat_score: int
    discovered_subdomains: List[str]
    detected_changes: List[ChangeDelta] = field(default_factory=list)
    scanned_at: datetime = field(default_factory=datetime.utcnow)
