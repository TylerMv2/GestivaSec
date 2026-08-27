"""
Gestiva Security (GestivaSec V1) — Event Collector Manager Application Service
Orchestrates high-throughput event ingestion, Asset Resolver matching, EPS calculation, and buffer management.
"""
import time
from typing import List, Dict, Any, Optional
from backend.domain.collector import RawEventRecord, CollectorMetrics
from backend.infrastructure.asset_resolver import AssetResolver
from backend.infrastructure.collectors.base_collector import BaseCollector
from backend.infrastructure.collectors.concrete_collectors import (
    SyslogCollector, WindowsEventCollector, JsonCollector, WebhookCollector, AgentCollector
)

_INGESTED_RAW_EVENTS: List[RawEventRecord] = []

class CollectorManagerService:
    def __init__(self):
        self.collectors: Dict[str, BaseCollector] = {
            "SYSLOG": SyslogCollector(),
            "WINDOWS_EVTX": WindowsEventCollector(),
            "REST_JSON": JsonCollector(),
            "CLOUD_WEBHOOK": WebhookCollector(),
            "GESTIVASEC_AGENT": AgentCollector()
        }

    async def ingest_event(
        self,
        collector_type: str,
        payload: Dict[str, Any],
        organization_id: str
    ) -> RawEventRecord:
        """Ingests raw event through registered collector plugin."""
        collector = self.collectors.get(collector_type.upper())
        if not collector:
            # Fallback to REST_JSON if unknown type
            collector = self.collectors["REST_JSON"]

        record = await collector.process_raw_payload(payload, organization_id)
        _INGESTED_RAW_EVENTS.append(record)
        return record

    async def list_raw_events(self, organization_id: str, limit: int = 50) -> List[RawEventRecord]:
        """Returns raw events ingested for organization (BR-0004)."""
        filtered = [e for e in _INGESTED_RAW_EVENTS if e.organization_id == organization_id]
        return filtered[-limit:]

    def get_collector_metrics(self) -> List[CollectorMetrics]:
        """Returns EPS and health metrics across all 5 collector plugins."""
        return [c.get_metrics() for c in self.collectors.values()]
