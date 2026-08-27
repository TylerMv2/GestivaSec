"""
Gestiva Security (GestivaSec V1) — SPRINT 3: Asset Intelligence & Lifecycle Management
CMDB-Grade Asset Domain Aggregate encapsulating Asset UUID, IP/Hostname History, Lifecycle State Machine, and Exposure Risk Scoring.
Enforces Business Rules BR-02 (Owner Email Required) and BR-04 (Tenant Isolation).
"""
import uuid
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from shared.constants import AssetStatus, BR02_OWNER_REQUIRED_FOR_ASSET

@dataclass
class IPHistoryRecord:
    ip_address: str
    assigned_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class DigitalAsset:
    id: Optional[str]
    organization_id: str
    name: str
    target_url: str
    criticality: str
    owner_email: str
    status: AssetStatus = AssetStatus.ACTIVE
    department: str = "IT & Security Operations"
    business_unit: str = "Core Infrastructure"
    os_family: str = "Linux / Unix"
    mac_addresses: List[str] = field(default_factory=list)
    cloud_resource_id: Optional[str] = None
    fingerprint_confidence: float = 0.95
    risk_score: float = 15.0
    tags: List[str] = field(default_factory=lambda: ["core", "production"])
    ip_history: List[IPHistoryRecord] = field(default_factory=list)
    installed_services: List[str] = field(default_factory=list)
    last_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    created_at: Optional[datetime] = None

    def __post_init__(self):
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now(timezone.utc)
        self.validate()

    def validate(self) -> None:
        """Enforces domain invariants."""
        if not self.organization_id or not self.organization_id.strip():
            raise ValueError("BR-04 Violation: Organization ID is required for multi-tenant isolation.")
        
        if not self.name or not self.name.strip():
            raise ValueError("Asset name cannot be empty.")
            
        if not self.target_url or not self.target_url.strip():
            raise ValueError("Target URL cannot be empty.")
            
        if BR02_OWNER_REQUIRED_FOR_ASSET:
            if not self.owner_email or not self.owner_email.strip():
                raise ValueError("BR-02 Violation: Every digital asset must have an assigned owner email.")
            email_regex = r"^[^@]+@[^@]+\.[^@]+$"
            if not re.match(email_regex, self.owner_email.strip()):
                raise ValueError("BR-02 Violation: Owner email format is invalid.")

    def update_location(self, new_url_or_ip: str) -> None:
        """Updates IP/URL location and appends to forensic history log."""
        if self.target_url != new_url_or_ip:
            self.ip_history.append(IPHistoryRecord(ip_address=self.target_url))
            self.target_url = new_url_or_ip
            self.last_seen = datetime.now(timezone.utc)

    def transition_lifecycle(self, new_status: AssetStatus) -> None:
        """Lifecycle state machine transition."""
        self.status = new_status
        self.last_seen = datetime.now(timezone.utc)

    def calculate_risk_score(self) -> float:
        """Calculates exposure risk score (0 - 100) based on criticality and services."""
        base_score = 10.0
        if self.criticality == "P1_CRITICAL":
            base_score = 50.0
        elif self.criticality == "P2_HIGH":
            base_score = 35.0
        elif self.criticality == "P3_MEDIUM":
            base_score = 20.0

        service_factor = len(self.installed_services) * 5.0
        self.risk_score = min(100.0, base_score + service_factor)
        return self.risk_score
