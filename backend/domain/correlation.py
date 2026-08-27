"""
Gestiva Security (GestivaSec V1) — SPRINT 7: Multi-Event Correlation Engine Domain Models
Pure domain models for Correlation Rules, Signals, Sliding Time-Window Attack Chains, and Explainable Scoring.
"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

@dataclass
class CorrelationRule:
    rule_id: str = field(default_factory=lambda: f"CORR-RULE-{uuid.uuid4().hex[:8].upper()}")
    organization_id: str = "00000000-0000-0000-0000-000000000001"
    name: str = "Multi-Stage MITRE Attack Chain Correlation Strategy"
    description: str = "Correlates findings across asset UUID, IP address, and MITRE kill chain phases within a 15m window."
    enabled: bool = True
    version: str = "v1.0"
    time_window_minutes: int = 15
    required_event_count: int = 2
    severity: str = "P1_CRITICAL"
    mitre_attack_techniques: List[str] = field(default_factory=lambda: ["T1110.001", "T1068", "T1071", "T1041"])
    confidence_threshold: float = 0.70

@dataclass
class CorrelationSignal:
    signal_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str = ""
    signal_type: str = "FINDING"         # NORMALIZED_EVENT, FINDING, ALERT
    source_entity_id: str = ""
    asset_id: Optional[str] = None
    source_ip: str = "127.0.0.1"
    destination_ip: Optional[str] = None
    user_identity: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class AttackChainNode:
    node_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    finding_id: str = ""
    rule_id: str = ""
    rule_title: str = ""
    severity: str = "P1_CRITICAL"
    mitre_phase: str = "EXPLOITATION"   # RECONNAISSANCE, EXPLOITATION, PRIVILEGE_ESCALATION, EXFILTRATION
    asset_id: Optional[str] = None
    source_ip: str = "127.0.0.1"
    destination_ip: Optional[str] = None
    user_identity: Optional[str] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class AttackChain:
    chain_id: str = field(default_factory=lambda: f"CHAIN-{uuid.uuid4().hex[:8].upper()}")
    organization_id: str = ""
    asset_id: Optional[str] = None
    target_ip: str = "127.0.0.1"
    chain_title: str = "Multi-Stage Cyber Attack Sequence Detected"
    severity: str = "P1_CRITICAL"
    status: str = "ACTIVE"              # ACTIVE, CONTAINED, RESOLVED
    correlation_score: int = 87          # Deterministic 0-100 score
    confidence_score: float = 0.90
    explainable_reasons: List[str] = field(default_factory=list)
    nodes: List[AttackChainNode] = field(default_factory=list)
    kill_chain_stages: List[str] = field(default_factory=list)
    timeline: List[Dict[str, Any]] = field(default_factory=list)
    first_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    last_seen: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
