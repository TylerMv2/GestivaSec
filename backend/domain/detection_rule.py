"""
Gestiva Security (GestivaSec V1) — SPRINT 6: Detection Engine Domain Models
Pure domain models for Detection Rules, Findings, and Actionable Alerts.
"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

@dataclass
class DetectionRuleCondition:
    field_path: str = "event.action"    # e.g., "event.action", "source.ip", "source.geo_country"
    operator: str = "EQUALS"             # EQUALS, CONTAINS, REGEX, THRESHOLD
    target_value: Any = "LOGIN_FAILED"
    threshold_count: int = 1
    time_window_seconds: int = 60

@dataclass
class DetectionRule:
    rule_id: str = field(default_factory=lambda: f"RULE-{uuid.uuid4().hex[:8].upper()}")
    title: str = "Brute Force Authentication Attempt Detected"
    description: str = "Triggers when multiple authentication failures occur against an asset."
    severity: str = "P1_CRITICAL"       # P1_CRITICAL, P2_HIGH, P3_MEDIUM, P4_LOW
    category: str = "AUTHENTICATION"   # AUTHENTICATION, NETWORK, PROCESS, SYSTEM
    mitre_attack_id: str = "T1110.001"  # MITRE ATT&CK Technique
    condition: DetectionRuleCondition = field(default_factory=DetectionRuleCondition)
    active: bool = True
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class Finding:
    finding_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str = ""
    rule_id: str = ""
    rule_title: str = ""
    severity: str = "P1_CRITICAL"
    asset_id: Optional[str] = None
    source_ip: str = "127.0.0.1"
    matched_event_ids: List[str] = field(default_factory=list)
    confidence_score: float = 0.95
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class ActionableAlert:
    alert_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str = ""
    rule_id: str = ""
    title: str = ""
    severity: str = "P1_CRITICAL"
    asset_id: Optional[str] = None
    source_ip: str = "127.0.0.1"
    status: str = "NEW"                 # NEW, IN_PROGRESS, CONTAINED, DISMISSED
    mitre_attack_id: str = "T1110.001"
    findings_count: int = 1
    first_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
