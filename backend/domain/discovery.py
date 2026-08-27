"""
Gestiva Security (GestivaSec V1) — SPRINT 2: Asset Discovery Domain Model
Encapsulates Discovered Host, Open Ports, OS Fingerprints, and Discovery Scan Jobs.
"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

@dataclass
class DiscoveredPort:
    port: int
    protocol: str = "TCP"
    service_name: str = "unknown"
    banner: str = ""
    status: str = "OPEN"

@dataclass
class DiscoveredHost:
    host_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str = ""
    ip_address: str = ""
    hostname: str = ""
    os_family: str = "Linux / Unix"
    mac_address: str = ""
    vendor: str = "Generic Network Device"
    latency_ms: float = 0.0
    open_ports: List[DiscoveredPort] = field(default_factory=list)
    discovery_method: str = "SYN_STEALTH_PASSIVE"
    first_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_registered: bool = False

@dataclass
class DiscoveryScanJob:
    job_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str = ""
    target_cidr: str = "127.0.0.1/32"
    status: str = "COMPLETED"
    total_hosts_found: int = 0
    scan_duration_ms: float = 0.0
    hosts: List[DiscoveredHost] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
