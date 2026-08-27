"""
Gestiva Security (GestivaSec V1) — SPRINT 10: SOAR Engine Domain Models
Pure domain models for Playbooks, Playbook Steps, Executions, Approval Requests, Rollback Records, and Response Actions.
"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

class ActionRiskLevel:
    LOW = "LOW"             # Automatic execution allowed (Enrichment, Comment, Timeline, Notification)
    MEDIUM = "MEDIUM"       # Approval required by default (Block IP, Block Domain, Revoke Session)
    HIGH = "HIGH"           # Mandatory human approval (Isolate Host, Disable User)
    CRITICAL = "CRITICAL"   # Multi-asset / Multi-tenant (Mandatory approval + scope confirmation)

class PlaybookStatus:
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    DISABLED = "DISABLED"
    ARCHIVED = "ARCHIVED"

class ExecutionStatus:
    PENDING = "PENDING"
    APPROVAL_REQUIRED = "APPROVAL_REQUIRED"
    APPROVED = "APPROVED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    SIMULATED = "SIMULATED"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"
    ROLLED_BACK = "ROLLED_BACK"
    PARTIALLY_COMPLETED = "PARTIALLY_COMPLETED"

class ApprovalStatus:
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"

# Allowed Action Types
ALLOWED_ACTION_TYPES = [
    "ENRICH_INDICATOR",
    "LOOKUP_THREAT_INTEL",
    "CREATE_INCIDENT_TIMELINE_ENTRY",
    "ADD_INCIDENT_COMMENT",
    "NOTIFY_ANALYST",
    "NOTIFY_SOC_LEAD",
    "REQUEST_APPROVAL",
    "ISOLATE_HOST",
    "BLOCK_IP",
    "BLOCK_DOMAIN",
    "DISABLE_USER",
    "REVOKE_SESSION",
    "COLLECT_FORENSIC_METADATA",
    "RUN_HEALTH_CHECK",
    "ISOLATE_ASSET",
    "BLOCK_FIREWALL_IP",
    "DISPATCH_NOTIFICATION"
]

@dataclass
class PlaybookStep:
    step_id: str = field(default_factory=lambda: f"STEP-{uuid.uuid4().hex[:6].upper()}")
    action_type: str = "ISOLATE_HOST"     # One of ALLOWED_ACTION_TYPES
    adapter_name: str = "MockEDRAdapter"
    target_param: str = "asset_id"
    description: str = "Isolates network interfaces of target asset."
    risk_level: str = ActionRiskLevel.HIGH
    requires_approval: bool = True

@dataclass
class Playbook:
    playbook_id: str = field(default_factory=lambda: f"PB-{uuid.uuid4().hex[:8].upper()}")
    organization_id: str = "GLOBAL"       # GLOBAL or tenant UUID
    name: str = "Automated Host Isolation Playbook"
    title: str = "Automated Host Isolation Playbook"
    description: str = "Triggers immediate containment upon P1 Critical Threat detection."
    version: str = "1.0.0"
    status: str = PlaybookStatus.ACTIVE
    trigger_type: str = "P1_CRITICAL_ALERT" # P1_CRITICAL_ALERT, ATTACK_CHAIN, THREAT_INTEL_MATCH, MANUAL
    trigger_event: str = "P1_CRITICAL_ALERT"
    severity_threshold: str = "P1_CRITICAL"
    requires_approval: bool = True
    steps: List[PlaybookStep] = field(default_factory=list)
    actions: List[Any] = field(default_factory=list) # For backward compatibility
    active: bool = True
    created_by: str = "soc-admin@gestivaone.com"
    updated_by: str = "soc-admin@gestivaone.com"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class PlaybookExecutionStep:
    execution_step_id: str = field(default_factory=lambda: f"EXSTEP-{uuid.uuid4().hex[:8].upper()}")
    execution_id: str = ""
    step_id: str = ""
    action_type: str = "ISOLATE_HOST"
    adapter: str = "MockEDRAdapter"
    status: str = "SUCCESS"               # SUCCESS, FAILED, SKIPPED, CANCELLED, ROLLED_BACK
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    request_reference: Dict[str, Any] = field(default_factory=dict)
    response_reference: Dict[str, Any] = field(default_factory=dict)
    error_message: Optional[str] = None
    rollback_available: bool = True
    rollback_status: Optional[str] = None

@dataclass
class PlaybookExecution:
    execution_id: str = field(default_factory=lambda: f"EXEC-{uuid.uuid4().hex[:8].upper()}")
    organization_id: str = "00000000-0000-0000-0000-000000000001"
    playbook_id: str = ""
    playbook_version: str = "1.0.0"
    incident_id: Optional[str] = None
    case_id: Optional[str] = None
    target_resource: str = ""
    trigger_source: str = "MANUAL"
    status: str = ExecutionStatus.PENDING # PENDING, APPROVAL_REQUIRED, RUNNING, COMPLETED, FAILED, CANCELLED, ROLLED_BACK
    initiated_by: str = "SOAR_AUTOMATION_ENGINE"
    approval_status: str = ApprovalStatus.APPROVED
    rollback_status: Optional[str] = None
    execution_context: Dict[str, Any] = field(default_factory=dict)
    failure_reason: Optional[str] = None
    executed_steps: List[PlaybookExecutionStep] = field(default_factory=list)
    action_results: List[Dict[str, Any]] = field(default_factory=list)
    started_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    completed_at: Optional[datetime] = None
    timestamp: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class ApprovalRequest:
    approval_id: str = field(default_factory=lambda: f"APP-{uuid.uuid4().hex[:8].upper()}")
    organization_id: str = "00000000-0000-0000-0000-000000000001"
    execution_id: str = ""
    requested_action: str = "ISOLATE_HOST"
    requested_by: str = "system@gestivaone.com"
    approved_by: Optional[str] = None
    status: str = ApprovalStatus.PENDING
    requested_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    resolved_at: Optional[datetime] = None
    rejection_reason: Optional[str] = None

@dataclass
class RollbackRecord:
    rollback_id: str = field(default_factory=lambda: f"ROLL-{uuid.uuid4().hex[:8].upper()}")
    execution_id: str = ""
    execution_step_id: str = ""
    action_type: str = "ISOLATE_HOST"
    rollback_action: str = "UNISOLATE_HOST"
    status: str = "COMPLETED"             # COMPLETED, FAILED
    initiated_by: str = "soc-admin@gestivaone.com"
    completed_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

# Legacy backward-compatibility class alias
@dataclass
class PlaybookAction:
    action_type: str = "ISOLATE_ASSET"
    target_param: str = "asset_id"
    description: str = "Isolates compromised host network interfaces."

@dataclass
class PlaybookExecutionRecord(PlaybookExecution):
    playbook_title: str = "Automated Host Isolation Playbook"
    executed_by: str = "SOAR_AUTOMATION_ENGINE"
