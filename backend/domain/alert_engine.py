"""
Gestiva Security (GestivaSec V1) — Security Alert Engine & Timeline Domain Model (CAP-05, CAP-07, CAP-08)
Encapsulates Rule-based Alerting, Chronological Timeline Events, and Incident Center Lifecycles.
"""
from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class AlertSeverity(str, Enum):
    INFO = "INFO"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    WARNING = "WARNING"
    CRITICAL = "CRITICAL"

class IncidentStatus(str, Enum):
    NEW = "NEW"
    INVESTIGATING = "INVESTIGATING"
    CONTAINED = "CONTAINED"
    MITIGATED = "MITIGATED"
    CLOSED_WITH_RCA = "CLOSED_WITH_RCA"

@dataclass
class SecurityAlert:
    id: str
    asset_id: str
    target_url: str
    rule_name: str
    severity: AlertSeverity
    message: str
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class TimelineEvent:
    id: str
    event_type: str  # "DISCOVERY", "ALERT", "MODIFICATION", "INCIDENT"
    source: str
    description: str
    severity: str
    timestamp: datetime = field(default_factory=datetime.utcnow)

@dataclass
class SOCIncident:
    id: str
    alert_id: str
    title: str
    severity: AlertSeverity
    status: IncidentStatus
    assigned_to: str
    notes: List[str] = field(default_factory=list)
    rca_report: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

    def transition_status(self, new_status: IncidentStatus, rca_report: Optional[str] = None):
        if new_status == IncidentStatus.CLOSED_WITH_RCA and not rca_report:
            raise ValueError("Regla BR-0001: Cierre de incidente P1 exige informe de Causa Raíz (RCA).")
        self.status = new_status
        if rca_report:
            self.rca_report = rca_report
