"""
Gestiva Security (GestivaSec V1) — SPRINT 8: Incident & Case Management Domain Models
Pure domain models for Operational Incidents, Investigation Cases, Evidence Timelines, Comments, SLA Tracking, and RCA.
"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional

@dataclass
class IncidentEvidence:
    evidence_id: str = field(default_factory=lambda: f"EVID-{uuid.uuid4().hex[:8].upper()}")
    organization_id: str = "00000000-0000-0000-0000-000000000001"
    incident_id: str = ""
    case_id: Optional[str] = None
    source_type: str = "GES_EVENT"       # GES_EVENT, FINDING, ALERT, ATTACK_CHAIN, ASSET, FILE_HASH, IP_ADDRESS
    source_id: str = ""
    description: str = ""
    payload: Dict[str, Any] = field(default_factory=dict)
    added_by: str = "analyst@gestivaone.com"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    hash_reference: str = field(default_factory=lambda: uuid.uuid4().hex)

@dataclass
class IncidentTimelineEntry:
    entry_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str = "00000000-0000-0000-0000-000000000001"
    incident_id: str = ""
    event_type: str = "STATUS_CHANGE"
    description: str = ""
    actor_id: str = "system@gestivaone.com"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    previous_state: Optional[str] = None
    new_state: Optional[str] = None

@dataclass
class IncidentComment:
    comment_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    organization_id: str = "00000000-0000-0000-0000-000000000001"
    incident_id: str = ""
    case_id: Optional[str] = None
    author_id: str = "analyst@gestivaone.com"
    content: str = ""
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class RootCauseAnalysis:
    rca_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    incident_id: str = ""
    root_cause: str = "Exposed SSH port with weak administrative credentials."
    attack_vector: str = "Brute Force Authentication"
    initial_access: str = "Credential Compromise"
    affected_assets: List[str] = field(default_factory=list)
    affected_users: List[str] = field(default_factory=list)
    impact: str = "Unauthorized shell access attempt contained."
    lessons_learned: str = "Enforce multi-factor authentication and fail2ban."
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class SLAState:
    sla_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    incident_id: str = ""
    target_deadline: datetime = field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=4))
    actual_completion: Optional[datetime] = None
    breached_status: bool = False
    remaining_seconds: int = 14400
    elapsed_seconds: int = 0

@dataclass
class EscalationRecord:
    escalation_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    incident_id: str = ""
    trigger_reason: str = "SLA Breach or High Severity Threshold"
    escalated_by: str = "system@gestivaone.com"
    escalated_to: str = "soc-lead@gestivaone.com"
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class Incident:
    incident_id: str = field(default_factory=lambda: f"INC-{uuid.uuid4().hex[:8].upper()}")
    organization_id: str = "00000000-0000-0000-0000-000000000001"
    incident_number: int = 1001
    title: str = "P1 Critical Security Incident"
    description: str = "Correlated attack sequence requiring SOC Tier 2 intervention."
    source: str = "CORRELATION_ENGINE"
    origin_type: str = "ATTACK_CHAIN"   # ATTACK_CHAIN, CANDIDATE, ALERT, FINDING, MANUAL
    source_reference: str = ""
    severity: str = "P1_CRITICAL"       # P1_CRITICAL, P2_HIGH, P3_MEDIUM, P4_LOW
    priority: str = "P1"                # P1, P2, P3, P4
    status: str = "NEW"                 # NEW, ACKNOWLEDGED, TRIAGED, INVESTIGATING, CONTAINMENT, ERADICATION, RECOVERY, RESOLVED, CLOSED, CANCELLED
    category: str = "AUTHENTICATION"
    assigned_to: Optional[str] = None
    assigned_team: Optional[str] = "SOC Tier 2"
    asset_id: Optional[str] = None
    target_ip: Optional[str] = "127.0.0.1"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    detected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    acknowledged_at: Optional[datetime] = None
    investigating_at: Optional[datetime] = None
    resolved_at: Optional[datetime] = None
    closed_at: Optional[datetime] = None
    sla_deadline: datetime = field(default_factory=lambda: datetime.now(timezone.utc) + timedelta(hours=4))
    resolution_summary: Optional[str] = None
    root_cause: Optional[str] = None
    closure_reason: Optional[str] = None

    def can_transition_to(self, new_status: str) -> bool:
        valid_transitions = {
            "NEW": ["ACKNOWLEDGED", "TRIAGED", "INVESTIGATING", "CANCELLED"],
            "ACKNOWLEDGED": ["TRIAGED", "INVESTIGATING", "CANCELLED"],
            "TRIAGED": ["INVESTIGATING", "CONTAINMENT", "RESOLVED", "CANCELLED"],
            "INVESTIGATING": ["CONTAINMENT", "ERADICATION", "RECOVERY", "RESOLVED", "CLOSED", "CLOSED_WITH_RCA", "CANCELLED"],
            "CONTAINMENT": ["ERADICATION", "RECOVERY", "RESOLVED"],
            "ERADICATION": ["RECOVERY", "RESOLVED"],
            "RECOVERY": ["RESOLVED"],
            "RESOLVED": ["CLOSED", "INVESTIGATING"],
            "CLOSED": ["NEW"], # Reopen
            "CANCELLED": []
        }
        return new_status.upper() in valid_transitions.get(self.status, [])

@dataclass
class IncidentCase:
    case_id: str = field(default_factory=lambda: f"CASE-{uuid.uuid4().hex[:8].upper()}")
    organization_id: str = "00000000-0000-0000-0000-000000000001"
    incident_id: str = ""
    case_number: int = 5001
    title: str = "Forensic Investigation Case Workspace"
    status: str = "OPEN"                 # OPEN, IN_PROGRESS, BLOCKED, PENDING_EXTERNAL, RESOLVED, CLOSED, CANCELLED
    assigned_to: Optional[str] = "tier2@gestivaone.com"
    assigned_team: Optional[str] = "Forensics"
    priority: str = "P1"
    description: str = "Correlated attack sequence requiring SOC Tier 2 intervention."
    severity: str = "P1_CRITICAL"
    assigned_analyst_email: Optional[str] = "tier2@gestivaone.com"
    asset_id: Optional[str] = None
    target_ip: Optional[str] = None
    attack_chain_id: Optional[str] = None
    evidence_timeline: List[IncidentEvidence] = field(default_factory=list)
    rca_summary: Optional[str] = None
    remediation_actions: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    closed_at: Optional[datetime] = None

    def can_transition_to(self, new_status: str) -> bool:
        valid_transitions = {
            "OPEN": ["IN_PROGRESS", "BLOCKED", "PENDING_EXTERNAL", "CANCELLED"],
            "IN_PROGRESS": ["BLOCKED", "PENDING_EXTERNAL", "RESOLVED", "CLOSED", "CANCELLED"],
            "BLOCKED": ["IN_PROGRESS", "CANCELLED"],
            "PENDING_EXTERNAL": ["IN_PROGRESS", "CANCELLED"],
            "RESOLVED": ["CLOSED", "IN_PROGRESS"],
            "CLOSED": [],
            "CANCELLED": []
        }
        return new_status.upper() in valid_transitions.get(self.status, [])
