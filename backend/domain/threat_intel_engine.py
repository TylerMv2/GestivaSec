"""
Gestiva Security (GestivaSec V1) — SPRINT 9: Threat Intelligence & Enrichment Engine Domain Models
Pure domain models for Threat Indicators, Threat Intel Sources, Matches, Enrichments, IoCs, and YARA Pattern Matches.
"""
import uuid
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

class IndicatorType:
    IP_ADDRESS = "IP_ADDRESS"
    DOMAIN = "DOMAIN"
    HOSTNAME = "HOSTNAME"
    URL = "URL"
    FILE_HASH_MD5 = "FILE_HASH_MD5"
    FILE_HASH_SHA1 = "FILE_HASH_SHA1"
    FILE_HASH_SHA256 = "FILE_HASH_SHA256"
    EMAIL = "EMAIL"
    CVE = "CVE"
    ASN = "ASN"

class IndicatorStatus:
    ACTIVE = "ACTIVE"
    EXPIRED = "EXPIRED"
    REVOKED = "REVOKED"
    DISABLED = "DISABLED"

class ReputationScore:
    UNKNOWN = "UNKNOWN"
    BENIGN = "BENIGN"
    SUSPICIOUS = "SUSPICIOUS"
    MALICIOUS = "MALICIOUS"

@dataclass
class ThreatIntelSource:
    source_id: str = field(default_factory=lambda: f"SRC-{uuid.uuid4().hex[:8].upper()}")
    name: str = "INTERNAL"               # INTERNAL, MANUAL, OPEN_SOURCE, COMMERCIAL, GOVERNMENT, COMMUNITY
    source_type: str = "OPEN_SOURCE"     # MISP, OpenCTI, OTX, VirusTotal, AbuseIPDB, CISA_KEV, Manual
    description: str = "Threat intelligence source feed"
    is_active: bool = True
    credentials_configured: bool = False
    status: str = "IMPLEMENTED"          # IMPLEMENTED, ADAPTER_READY, PLANNED, NOT_IMPLEMENTED

@dataclass
class ThreatIndicator:
    indicator_id: str = field(default_factory=lambda: f"IND-{uuid.uuid4().hex[:8].upper()}")
    organization_id: str = "GLOBAL"       # GLOBAL or tenant UUID
    indicator_type: str = IndicatorType.IP_ADDRESS
    indicator_value: str = ""             # Original value
    normalized_value: str = ""           # Normalized canonical value
    source: str = "INTERNAL"
    source_reference: Optional[str] = None
    confidence: float = 0.90             # 0.0 to 1.0
    severity: str = "HIGH"               # LOW, MEDIUM, HIGH, CRITICAL
    reputation: str = ReputationScore.MALICIOUS # UNKNOWN, BENIGN, SUSPICIOUS, MALICIOUS
    status: str = IndicatorStatus.ACTIVE # ACTIVE, EXPIRED, REVOKED, DISABLED
    first_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    expires_at: Optional[datetime] = None
    tags: List[str] = field(default_factory=list)
    mitre_techniques: List[str] = field(default_factory=list)
    kill_chain_phases: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @staticmethod
    def normalize_value(indicator_type: str, raw_value: str) -> str:
        """Deterministic normalization engine for observables."""
        val = raw_value.strip()
        t = indicator_type.upper()
        if t in [IndicatorType.DOMAIN, IndicatorType.HOSTNAME]:
            val = val.lower().rstrip('.')
            val = val.replace('[.]', '.').replace('(:)', ':')
        elif t in [IndicatorType.IP_ADDRESS]:
            val = val.replace('[.]', '.')
        elif t in [IndicatorType.URL]:
            val = val.replace('hxxp', 'http').replace('[.]', '.')
        elif t in [IndicatorType.FILE_HASH_MD5, IndicatorType.FILE_HASH_SHA1, IndicatorType.FILE_HASH_SHA256]:
            val = val.lower()
        elif t in [IndicatorType.EMAIL]:
            val = val.lower()
        return val

@dataclass
class ThreatIntelMatch:
    match_id: str = field(default_factory=lambda: f"MATCH-{uuid.uuid4().hex[:8].upper()}")
    indicator_id: str = ""
    observable_type: str = IndicatorType.IP_ADDRESS
    observable_value: str = ""
    matched_entity_type: str = "NORMALIZED_EVENT" # NORMALIZED_EVENT, FINDING, ALERT, ATTACK_CHAIN, INCIDENT, CASE
    matched_entity_id: str = ""
    match_type: str = "EXACT"
    confidence: float = 0.90
    reputation: str = ReputationScore.MALICIOUS
    source: str = "INTERNAL"
    matched_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class ThreatIntelEnrichment:
    enrichment_id: str = field(default_factory=lambda: f"ENRICH-{uuid.uuid4().hex[:8].upper()}")
    entity_type: str = "NORMALIZED_EVENT"
    entity_id: str = ""
    matches: List[ThreatIntelMatch] = field(default_factory=list)
    composite_threat_score: float = 0.0
    threat_grade: str = "SAFE"           # SAFE, LOW, MEDIUM, HIGH, CRITICAL
    enriched_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

# --- BACKWARD COMPATIBILITY DOMAIN ENTITIES ---
@dataclass
class IndicatorOfCompromise:
    ioc_id: str = field(default_factory=lambda: f"IOC-{uuid.uuid4().hex[:8].upper()}")
    ioc_type: str = "IP_REPUTATION"      # IP_REPUTATION, DOMAIN_MALICIOUS, FILE_HASH_SHA256
    value: str = ""
    threat_score: float = 85.0
    threat_actor: str = "APT-29 / Cozy Bear"
    confidence: float = 0.95
    category: str = "C2_SERVER"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class YaraMatchResult:
    rule_name: str = "Suspicious_Shellcode_Pattern"
    matched_strings: List[str] = field(default_factory=list)
    severity: str = "CRITICAL"
    description: str = "Payload contains obfuscated reverse shell shellcode pattern."
