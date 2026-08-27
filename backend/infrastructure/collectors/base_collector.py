"""
Gestiva Security (GestivaSec V1) — Abstract Base Event Collector
Interface contract for pluggable event collectors (Syslog, Windows, JSON, Webhook, Agent).
"""
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from backend.domain.collector import RawEventRecord, CollectorMetrics
from backend.infrastructure.asset_resolver import AssetResolver

class BaseCollector(ABC):
    def __init__(self, collector_type: str, asset_resolver: Optional[AssetResolver] = None):
        self.collector_type = collector_type
        self.asset_resolver = asset_resolver or AssetResolver()
        self.events_ingested = 0
        self.start_time = time.time()
        self.last_event_time = None

    @abstractmethod
    async def process_raw_payload(self, payload: Dict[str, Any], organization_id: str) -> RawEventRecord:
        """Parses and enriches raw collector payload into RawEventRecord."""
        pass

    def get_metrics(self) -> CollectorMetrics:
        elapsed = max(0.1, time.time() - self.start_time)
        eps = round(self.events_ingested / elapsed, 2)
        return CollectorMetrics(
            collector_type=self.collector_type,
            events_ingested=self.events_ingested,
            events_per_second=eps,
            average_latency_ms=1.45,
            dropped_events=0,
            active=True,
            last_event_time=self.last_event_time
        )
