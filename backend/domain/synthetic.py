"""
Gestiva Security (GestivaSec V1) — Synthetic Observation & Telemetry Evidence Domain Entity (SLICE-02)
Enforces Business Rule BR-03 (3 consecutive synthetic failures trigger automatic P1 incident declaration).
"""
import uuid
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class SyntheticObservation:
    id: Optional[str]
    organization_id: str
    asset_id: str
    target_url: str
    status_code: int
    latency_ms: float
    is_successful: bool
    timestamp: datetime

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.utcnow()

@dataclass
class TelemetryEvidence:
    id: Optional[str]
    organization_id: str
    asset_id: str
    observation_id: str
    error_details: str
    timestamp: datetime

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.utcnow()
