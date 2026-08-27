"""
Gestiva Security (GestivaSec V1) — IoC & Threat Indicator Registry Infrastructure Component
High-speed in-memory hashtable index for multi-tenant Threat Indicators and Indicators of Compromise.
"""
from typing import Dict, List, Optional
from datetime import datetime, timezone
from backend.domain.threat_intel_engine import (
    ThreatIndicator,
    IndicatorType,
    IndicatorStatus,
    ReputationScore,
    IndicatorOfCompromise
)

_DEFAULT_INDICATORS = [
    ThreatIndicator(
        indicator_id="IND-IP-MALICIOUS-01",
        organization_id="GLOBAL",
        indicator_type=IndicatorType.IP_ADDRESS,
        indicator_value="198.51.100.200",
        normalized_value="198.51.100.200",
        source="INTERNAL",
        confidence=0.98,
        severity="CRITICAL",
        reputation=ReputationScore.MALICIOUS,
        tags=["C2", "APT29"],
        mitre_techniques=["T1071.001"]
    ),
    ThreatIndicator(
        indicator_id="IND-DOMAIN-MALICIOUS-01",
        organization_id="GLOBAL",
        indicator_type=IndicatorType.DOMAIN,
        indicator_value="malicious-c2-node.com",
        normalized_value="malicious-c2-node.com",
        source="OPEN_SOURCE",
        confidence=0.92,
        severity="HIGH",
        reputation=ReputationScore.MALICIOUS,
        tags=["Phishing", "FIN7"],
        mitre_techniques=["T1566.002"]
    ),
    ThreatIndicator(
        indicator_id="IND-HASH-RANSOMWARE-01",
        organization_id="GLOBAL",
        indicator_type=IndicatorType.FILE_HASH_SHA256,
        indicator_value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        normalized_value="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
        source="COMMERCIAL",
        confidence=0.99,
        severity="CRITICAL",
        reputation=ReputationScore.MALICIOUS,
        tags=["Ransomware", "LockBit"],
        mitre_techniques=["T1486"]
    )
]

class IoCRegistry:
    def __init__(self):
        self._indicators: Dict[str, ThreatIndicator] = {}

        # Index structure: (indicator_type, normalized_value) -> List[ThreatIndicator]
        self._lookup_index: Dict[str, List[ThreatIndicator]] = {}

        # Seed defaults
        for ind in _DEFAULT_INDICATORS:
            self.add_indicator(ind)

    def add_indicator(self, indicator: ThreatIndicator) -> ThreatIndicator:
        """Indexes indicator in fast lookup hash tables."""
        if not indicator.normalized_value:
            indicator.normalized_value = ThreatIndicator.normalize_value(indicator.indicator_type, indicator.indicator_value)

        self._indicators[indicator.indicator_id] = indicator
        key = f"{indicator.indicator_type.upper()}:{indicator.normalized_value}"
        if key not in self._lookup_index:
            self._lookup_index[key] = []
        self._lookup_index[key].append(indicator)
        return indicator

    def get_indicator(self, indicator_id: str) -> Optional[ThreatIndicator]:
        return self._indicators.get(indicator_id)

    def list_indicators(self, organization_id: str, limit: int = 50) -> List[ThreatIndicator]:
        """Lists indicators accessible to organization_id (GLOBAL + tenant-specific)."""
        res = [ind for ind in self._indicators.values() if ind.organization_id in ["GLOBAL", organization_id]]
        return res[-limit:]

    def lookup_indicator(self, indicator_type: str, raw_value: str, organization_id: str = "GLOBAL") -> Optional[ThreatIndicator]:
        """High-speed exact match lookup (< 0.5ms) enforcing tenant isolation & active status."""
        norm_val = ThreatIndicator.normalize_value(indicator_type, raw_value)
        key = f"{indicator_type.upper()}:{norm_val}"
        candidates = self._lookup_index.get(key, [])
        now = datetime.now(timezone.utc)

        for ind in candidates:
            # Enforce status, expiration, and tenant boundary
            if ind.status == IndicatorStatus.ACTIVE:
                if ind.expires_at and ind.expires_at < now:
                    ind.status = IndicatorStatus.EXPIRED
                    continue
                if ind.organization_id in ["GLOBAL", organization_id]:
                    return ind
        return None

    def disable_indicator(self, indicator_id: str) -> Optional[ThreatIndicator]:
        ind = self.get_indicator(indicator_id)
        if ind:
            ind.status = IndicatorStatus.DISABLED
            ind.updated_at = datetime.now(timezone.utc)
        return ind

    def revoke_indicator(self, indicator_id: str) -> Optional[ThreatIndicator]:
        ind = self.get_indicator(indicator_id)
        if ind:
            ind.status = IndicatorStatus.REVOKED
            ind.updated_at = datetime.now(timezone.utc)
        return ind

    # Backward compatibility methods
    def add_ioc(self, ioc: IndicatorOfCompromise) -> IndicatorOfCompromise:
        ind_type = IndicatorType.IP_ADDRESS if ioc.ioc_type == "IP_REPUTATION" else (IndicatorType.DOMAIN if ioc.ioc_type == "DOMAIN_MALICIOUS" else IndicatorType.FILE_HASH_SHA256)
        ind = ThreatIndicator(
            indicator_id=ioc.ioc_id,
            organization_id="GLOBAL",
            indicator_type=ind_type,
            indicator_value=ioc.value,
            normalized_value=ThreatIndicator.normalize_value(ind_type, ioc.value),
            confidence=ioc.confidence,
            severity="CRITICAL" if ioc.threat_score > 90 else "HIGH",
            reputation=ReputationScore.MALICIOUS
        )
        self.add_indicator(ind)
        return ioc

    def lookup_ip(self, ip_address: str) -> Optional[IndicatorOfCompromise]:
        ind = self.lookup_indicator(IndicatorType.IP_ADDRESS, ip_address)
        if ind:
            return IndicatorOfCompromise(
                ioc_id=ind.indicator_id,
                ioc_type="IP_REPUTATION",
                value=ind.indicator_value,
                threat_score=ind.confidence * 100.0,
                confidence=ind.confidence
            )
        return None

    def lookup_domain(self, domain: str) -> Optional[IndicatorOfCompromise]:
        ind = self.lookup_indicator(IndicatorType.DOMAIN, domain)
        if ind:
            return IndicatorOfCompromise(
                ioc_id=ind.indicator_id,
                ioc_type="DOMAIN_MALICIOUS",
                value=ind.indicator_value,
                threat_score=ind.confidence * 100.0,
                confidence=ind.confidence
            )
        return None

    def lookup_hash(self, file_hash: str) -> Optional[IndicatorOfCompromise]:
        ind = self.lookup_indicator(IndicatorType.FILE_HASH_SHA256, file_hash)
        if ind:
            return IndicatorOfCompromise(
                ioc_id=ind.indicator_id,
                ioc_type="FILE_HASH_SHA256",
                value=ind.indicator_value,
                threat_score=ind.confidence * 100.0,
                confidence=ind.confidence
            )
        return None
