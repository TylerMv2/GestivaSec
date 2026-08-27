"""
Gestiva Security (GestivaSec V1) — SPRINT 9: Threat Intelligence & Enrichment Application Service
Provides high-speed Indicator CRUD, real-time telemetry matching (< 0.5ms), YARA pattern scanning, and immutable enrichment.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from backend.domain.normalized_event import NormalizedEvent
from backend.domain.threat_intel_engine import (
    ThreatIndicator,
    ThreatIntelSource,
    ThreatIntelMatch,
    ThreatIntelEnrichment,
    IndicatorType,
    IndicatorStatus,
    ReputationScore,
    IndicatorOfCompromise,
    YaraMatchResult
)
from backend.infrastructure.ioc_registry import IoCRegistry
from backend.infrastructure.yara_service import YaraScannerService
from backend.infrastructure.threat_intel_engine import ThreatIntelEngine
from backend.infrastructure.audit_repository import AuditRepository, AuditEvent

_SHARED_IOC_REGISTRY = IoCRegistry()
_SOURCES_REGISTRY: List[ThreatIntelSource] = [
    ThreatIntelSource(name="INTERNAL", source_type="Manual", description="Internal SOC analyst indicators", is_active=True, status="IMPLEMENTED"),
    ThreatIntelSource(name="OPEN_SOURCE", source_type="MISP", description="MISP Threat Sharing Platform", is_active=True, status="ADAPTER_READY"),
    ThreatIntelSource(name="COMMERCIAL", source_type="VirusTotal", description="VirusTotal Threat Intelligence API", is_active=True, status="ADAPTER_READY"),
    ThreatIntelSource(name="GOVERNMENT", source_type="CISA_KEV", description="CISA Known Exploited Vulnerabilities", is_active=True, status="ADAPTER_READY"),
]

class ThreatIntelApplicationService:
    def __init__(self, registry: Optional[IoCRegistry] = None, yara_scanner: Optional[YaraScannerService] = None, audit_repo: Optional[AuditRepository] = None):
        self.registry = registry or _SHARED_IOC_REGISTRY
        self.yara_scanner = yara_scanner or YaraScannerService()
        self.audit_repo = audit_repo or AuditRepository()

    # --- INDICATOR LIFECYCLE ---
    async def create_indicator(
        self,
        organization_id: str,
        indicator_type: str,
        indicator_value: str,
        source: str = "INTERNAL",
        confidence: float = 0.90,
        severity: str = "HIGH",
        reputation: str = ReputationScore.MALICIOUS,
        tags: Optional[List[str]] = None,
        mitre_techniques: Optional[List[str]] = None,
        actor_email: str = "analyst@gestivaone.com"
    ) -> ThreatIndicator:
        norm_val = ThreatIndicator.normalize_value(indicator_type, indicator_value)
        ind = ThreatIndicator(
            organization_id=organization_id,
            indicator_type=indicator_type.upper(),
            indicator_value=indicator_value,
            normalized_value=norm_val,
            source=source,
            confidence=confidence,
            severity=severity.upper(),
            reputation=reputation.upper(),
            tags=tags or [],
            mitre_techniques=mitre_techniques or []
        )
        added = self.registry.add_indicator(ind)

        # Audit Event
        await self.audit_repo.record_event(
            AuditEvent(
                actor_email=actor_email,
                organization_id=organization_id,
                action="INDICATOR_CREATED",
                resource_type="THREAT_INDICATOR",
                resource_id=added.indicator_id,
                details={"indicator_type": indicator_type, "normalized_value": norm_val}
            )
        )
        return added

    def get_indicator(self, indicator_id: str) -> Optional[ThreatIndicator]:
        return self.registry.get_indicator(indicator_id)

    def list_indicators(self, organization_id: str, limit: int = 50) -> List[ThreatIndicator]:
        return self.registry.list_indicators(organization_id, limit=limit)

    async def disable_indicator(self, indicator_id: str, actor_email: str = "analyst@gestivaone.com") -> Optional[ThreatIndicator]:
        ind = self.registry.disable_indicator(indicator_id)
        if ind:
            await self.audit_repo.record_event(
                AuditEvent(
                    actor_email=actor_email,
                    organization_id=ind.organization_id,
                    action="INDICATOR_DISABLED",
                    resource_type="THREAT_INDICATOR",
                    resource_id=ind.indicator_id,
                    details={"status": "DISABLED"}
                )
            )
        return ind

    async def revoke_indicator(self, indicator_id: str, actor_email: str = "analyst@gestivaone.com") -> Optional[ThreatIndicator]:
        ind = self.registry.revoke_indicator(indicator_id)
        if ind:
            await self.audit_repo.record_event(
                AuditEvent(
                    actor_email=actor_email,
                    organization_id=ind.organization_id,
                    action="INDICATOR_REVOKED",
                    resource_type="THREAT_INDICATOR",
                    resource_id=ind.indicator_id,
                    details={"status": "REVOKED"}
                )
            )
        return ind

    # --- LOOKUP & MATCHING ---
    def lookup_indicator(self, indicator_type: str, raw_value: str, organization_id: str = "GLOBAL") -> Optional[ThreatIndicator]:
        return self.registry.lookup_indicator(indicator_type, raw_value, organization_id)

    async def match_observables(
        self,
        observables: List[Dict[str, str]],
        entity_type: str = "NORMALIZED_EVENT",
        entity_id: str = "",
        organization_id: str = "GLOBAL"
    ) -> List[ThreatIntelMatch]:
        """Matches a list of observables ({'type': 'IP_ADDRESS', 'value': '1.2.3.4'}) against active TI."""
        matches: List[ThreatIntelMatch] = []
        for obs in observables:
            obs_type = obs.get("type", "").upper()
            obs_val = obs.get("value", "")
            if not (obs_type and obs_val): continue

            match_ind = self.lookup_indicator(obs_type, obs_val, organization_id)
            if match_ind:
                match = ThreatIntelMatch(
                    indicator_id=match_ind.indicator_id,
                    observable_type=obs_type,
                    observable_value=obs_val,
                    matched_entity_type=entity_type,
                    matched_entity_id=entity_id,
                    match_type="EXACT",
                    confidence=match_ind.confidence,
                    reputation=match_ind.reputation,
                    source=match_ind.source
                )
                matches.append(match)

                await self.audit_repo.record_event(
                    AuditEvent(
                        actor_email="system@gestivaone.com",
                        organization_id=organization_id,
                        action="THREAT_INTEL_MATCHED",
                        resource_type="THREAT_INTEL_MATCH",
                        resource_id=match.match_id,
                        details={"indicator_id": match_ind.indicator_id, "observable_value": obs_val}
                    )
                )

        return matches

    def enrich_entity(self, entity_type: str, entity_id: str, matches: List[ThreatIntelMatch]) -> ThreatIntelEnrichment:
        """Applies threat intelligence enrichment without mutating raw telemetry."""
        composite_score = max([m.confidence * 100.0 for m in matches], default=0.0)
        grade = "CRITICAL" if composite_score >= 90 else ("HIGH" if composite_score >= 70 else ("MEDIUM" if composite_score >= 40 else "SAFE"))

        return ThreatIntelEnrichment(
            entity_type=entity_type,
            entity_id=entity_id,
            matches=matches,
            composite_threat_score=composite_score,
            threat_grade=grade
        )

    # --- BACKWARD COMPATIBILITY ---
    def ingest_ioc(self, ioc: IndicatorOfCompromise) -> IndicatorOfCompromise:
        return self.registry.add_ioc(ioc)

    def lookup_ioc(self, ioc_type: str, value: str) -> Optional[IndicatorOfCompromise]:
        t = ioc_type.upper()
        if t == "IP_REPUTATION": return self.registry.lookup_ip(value)
        elif t == "DOMAIN_MALICIOUS": return self.registry.lookup_domain(value)
        elif t == "FILE_HASH_SHA256": return self.registry.lookup_hash(value)
        return None

    def enrich_normalized_event(self, event: NormalizedEvent) -> Optional[ThreatIntelMatch]:
        match_ip = self.registry.lookup_ip(event.source.ip)
        if match_ip:
            return ThreatIntelMatch(indicator_id=match_ip.ioc_id, observable_type="IP_ADDRESS", observable_value=event.source.ip, matched_entity_type="NORMALIZED_EVENT", matched_entity_id=event.event_id)
        if event.destination and event.destination.ip:
            match_dest = self.registry.lookup_ip(event.destination.ip)
            if match_dest:
                return ThreatIntelMatch(indicator_id=match_dest.ioc_id, observable_type="IP_ADDRESS", observable_value=event.destination.ip, matched_entity_type="NORMALIZED_EVENT", matched_entity_id=event.event_id)
        return None

    def scan_payload_yara(self, content: str) -> List[YaraMatchResult]:
        return self.yara_scanner.scan_content(content)

    async def enrich_asset(self, asset_id: str, domain: str, resolved_ip: str):
        return await ThreatIntelEngine.enrich_asset(asset_id, domain, resolved_ip)
