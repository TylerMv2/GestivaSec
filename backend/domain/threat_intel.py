"""
Gestiva Security (GestivaSec V1) — Threat Intelligence Domain Model (CAP-06)
Encapsulates Decoupled Public Feeds: VirusTotal, AbuseIPDB, GreyNoise, CISA KEV, and NVD.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

@dataclass
class VirusTotalIndicator:
    malicious_votes: int
    suspicious_votes: int
    reputation: int
    last_analysis_date: str

@dataclass
class AbuseIpDbIndicator:
    abuse_confidence_score: int
    total_reports: int
    is_whitelisted: bool
    last_reported_at: str

@dataclass
class GreyNoiseIndicator:
    is_noise: bool
    is_malicious: bool
    actor: str
    tags: List[str]

@dataclass
class CisaKevIndicator:
    is_known_exploited: bool
    cve_id: Optional[str]
    vulnerability_name: Optional[str]
    action_due_date: Optional[str]

@dataclass
class NvdCveIndicator:
    cve_id: str
    cvss_v3_score: float
    severity: str  # LOW, MEDIUM, HIGH, CRITICAL

@dataclass
class ThreatIntelReport:
    asset_id: str
    domain: str
    resolved_ip: str
    virustotal: VirusTotalIndicator
    abuseipdb: AbuseIpDbIndicator
    greynoise: GreyNoiseIndicator
    cisa_kev: CisaKevIndicator
    nvd_cves: List[NvdCveIndicator]
    composite_threat_score: int  # 0 (Clean) to 100 (Critical Risk)
    threat_grade: str  # SAFE, LOW, MEDIUM, HIGH, CRITICAL
    cached: bool = False
    updated_at: datetime = field(default_factory=datetime.utcnow)

    def calculate_threat_score(self) -> int:
        score = 0
        if self.virustotal.malicious_votes > 0:
            score += self.virustotal.malicious_votes * 25
        if self.abuseipdb.abuse_confidence_score > 0:
            score += int(self.abuseipdb.abuse_confidence_score * 0.4)
        if self.greynoise.is_malicious:
            score += 30
        if self.cisa_kev.is_known_exploited:
            score += 40
        for cve in self.nvd_cves:
            if cve.severity in ["HIGH", "CRITICAL"]:
                score += 20
        return min(score, 100)
