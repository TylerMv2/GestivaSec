"""
Gestiva Security (GestivaSec V1) — Event Normalization Application Service
Parses raw events into GestivaSec Event Schema (GES) with GeoIP enrichment and Asset Resolver matching.
"""
from typing import List, Dict, Any, Optional
from backend.domain.collector import RawEventRecord
from backend.domain.normalized_event import (
    NormalizedEvent, EventObserver, EventSource, EventDestination, EventClassification
)
from backend.infrastructure.enrichment_service import EventEnrichmentAdapter
from backend.infrastructure.asset_resolver import AssetResolver

_NORMALIZED_EVENTS_STORE: List[NormalizedEvent] = []

class EventNormalizationService:
    def __init__(self, enricher: Optional[EventEnrichmentAdapter] = None, asset_resolver: Optional[AssetResolver] = None):
        self.enricher = enricher or EventEnrichmentAdapter()
        self.asset_resolver = asset_resolver or AssetResolver()

    async def normalize_raw_event(self, raw_record: RawEventRecord) -> NormalizedEvent:
        """Parses and transforms RawEventRecord into GestivaSec Event Schema (GES)."""
        payload = raw_record.payload or {}
        collector_type = raw_record.collector_type.upper()
        
        # 1. GeoIP Enrichment
        source_ip = raw_record.source_ip
        geo_info = self.enricher.enrich_source_ip(source_ip)

        # 2. Asset Resolution
        asset_id = raw_record.resolved_asset_id
        if not asset_id:
            asset_id = await self.asset_resolver.resolve_asset_id(source_ip, raw_record.organization_id, raw_record.source_hostname)

        # 3. Categorization Logic per Collector Type
        category = "AUTHENTICATION"
        action = "LOGIN_FAILED"
        severity = "HIGH"
        outcome = "FAILURE"

        if collector_type == "WINDOWS_EVTX":
            event_id = payload.get("event_id", 4625)
            if event_id == 4625:
                category, action, severity, outcome = "AUTHENTICATION", "LOGIN_FAILED", "HIGH", "FAILURE"
            elif event_id == 4624:
                category, action, severity, outcome = "AUTHENTICATION", "LOGIN_SUCCESS", "LOW", "SUCCESS"
            elif event_id == 4672:
                category, action, severity, outcome = "AUTHENTICATION", "PRIVILEGE_ESCALATION", "CRITICAL", "SUCCESS"

        elif collector_type == "SYSLOG":
            msg = str(payload.get("message", "")).lower()
            if "fail" in msg or "invalid" in msg:
                category, action, severity, outcome = "AUTHENTICATION", "LOGIN_FAILED", "HIGH", "FAILURE"
            elif "accepted" in msg:
                category, action, severity, outcome = "AUTHENTICATION", "LOGIN_SUCCESS", "LOW", "SUCCESS"
            else:
                category, action, severity, outcome = "SYSTEM", "LOG_NOTICE", "INFORMATIONAL", "SUCCESS"

        elif collector_type == "CLOUD_WEBHOOK":
            category, action, severity, outcome = "CLOUD_AUDIT", "API_CALL", "MEDIUM", "SUCCESS"

        norm_event = NormalizedEvent(
            organization_id=raw_record.organization_id,
            raw_event_id=raw_record.raw_event_id,
            observer=EventObserver(
                collector_id=f"{collector_type.lower()}-01",
                collector_type=collector_type,
                ip_address="127.0.0.1"
            ),
            source=EventSource(
                ip=source_ip,
                hostname=raw_record.source_hostname,
                geo_country=geo_info["geo_country"],
                geo_city=geo_info["geo_city"],
                geo_asn=geo_info["geo_asn"]
            ),
            destination=EventDestination(
                ip=payload.get("destination_ip", "10.0.0.1"),
                asset_id=asset_id
            ),
            event=EventClassification(
                category=category,
                action=action,
                severity=severity,
                outcome=outcome,
                protocol=payload.get("protocol", "TCP")
            ),
            enrichment=geo_info
        )

        # Threat Intel Real-Time Enrichment (Sprint 9)
        try:
            from backend.application.threat_intel_service import ThreatIntelApplicationService
            ti_service = ThreatIntelApplicationService()
            ti_match = ti_service.enrich_normalized_event(norm_event)
            if ti_match:
                norm_event.enrichment["threat_intel"] = {
                    "matched_ioc": ti_match.ioc.value,
                    "threat_actor": ti_match.ioc.threat_actor,
                    "threat_score": ti_match.ioc.threat_score,
                    "confidence": ti_match.ioc.confidence
                }
                norm_event.event.severity = "CRITICAL"
        except Exception:
            pass

        _NORMALIZED_EVENTS_STORE.append(norm_event)
        
        # Async trigger detection engine evaluation (Sprint 6)
        try:
            from backend.application.detection_service import DetectionEngineService
            detection_engine = DetectionEngineService()
            await detection_engine.process_normalized_event(norm_event)
        except Exception:
            pass

        return norm_event

    async def list_normalized_events(self, organization_id: str, limit: int = 50) -> List[NormalizedEvent]:
        """Returns normalized events for tenant (BR-0004)."""
        filtered = [e for e in _NORMALIZED_EVENTS_STORE if e.organization_id == organization_id]
        return filtered[-limit:]
