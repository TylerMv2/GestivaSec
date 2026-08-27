"""
Gestiva Security (GestivaSec V1) — SPRINT 5: GestivaSec Event Schema (GES)
Pure Domain Model for Normalized Security Events.
"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, Optional

@dataclass
class EventObserver:
    collector_id: str = "collector-default"
    collector_type: str = "SYSLOG"
    ip_address: str = "127.0.0.1"

@dataclass
class EventSource:
    ip: str = "127.0.0.1"
    port: Optional[int] = None
    hostname: Optional[str] = None
    user_id: Optional[str] = None
    user_email: Optional[str] = None
    geo_country: str = "LOCAL"
    geo_city: str = "Internal"
    geo_asn: str = "AS0"

@dataclass
class EventDestination:
    ip: str = "127.0.0.1"
    port: Optional[int] = None
    hostname: Optional[str] = None
    asset_id: Optional[str] = None

@dataclass
class EventClassification:
    category: str = "AUTHENTICATION" # AUTHENTICATION, NETWORK, PROCESS, FILE_SYSTEM, MALWARE, SYSTEM
    action: str = "LOGIN_FAILED"      # LOGIN_FAILED, LOGIN_SUCCESS, PRIVILEGE_ESCALATION, CONNECTION_BLOCKED
    severity: str = "HIGH"            # LOW, MEDIUM, HIGH, CRITICAL
    outcome: str = "FAILURE"          # SUCCESS, FAILURE, UNKNOWN
    protocol: str = "TCP"

@dataclass
class NormalizedEvent:
    event_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str = ""
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    ingested_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    observer: EventObserver = field(default_factory=EventObserver)
    source: EventSource = field(default_factory=EventSource)
    destination: EventDestination = field(default_factory=EventDestination)
    event: EventClassification = field(default_factory=EventClassification)
    enrichment: Dict[str, Any] = field(default_factory=dict)
    raw_event_id: Optional[str] = None
