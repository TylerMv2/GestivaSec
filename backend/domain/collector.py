"""
Gestiva Security (GestivaSec V1) — SPRINT 4: Event Collectors Framework Domain Model
Encapsulates Raw Event Ingestion, Event Sources, Asset Resolver References, and Collector Metrics.
"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, Optional

@dataclass
class RawEventRecord:
    raw_event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str = ""
    collector_type: str = "SYSLOG"
    source_ip: str = "127.0.0.1"
    source_hostname: Optional[str] = None
    resolved_asset_id: Optional[str] = None
    payload: Dict[str, Any] = field(default_factory=dict)
    received_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class CollectorMetrics:
    collector_type: str
    events_ingested: int = 0
    events_per_second: float = 0.0
    average_latency_ms: float = 0.0
    dropped_events: int = 0
    active: bool = True
    last_event_time: Optional[datetime] = None
