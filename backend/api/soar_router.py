"""
Gestiva Security (GestivaSec V1) — SPRINT 10: SOAR Engine REST API Router
Exposes comprehensive REST API for Playbooks, Execution Engine, Approval Gates, Rollback, and Audit History.
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field

from backend.application.soar_service import SoarApplicationService

router = APIRouter(tags=["SOAR Engine & Automated Response"])
soar_service = SoarApplicationService()

# --- REQUEST / DTO MODELS ---
class CreatePlaybookStepRequest(BaseModel):
    action_type: str = Field("ISOLATE_HOST", json_schema_extra={"example": "ISOLATE_HOST"})
    adapter_name: str = Field("MockEDRAdapter", json_schema_extra={"example": "MockEDRAdapter"})
    target_param: str = Field("asset_id", json_schema_extra={"example": "asset_id"})
    description: str = Field("Isolates network interface", json_schema_extra={"example": "Isolates network interface"})
    risk_level: str = Field("HIGH", json_schema_extra={"example": "HIGH"})
    requires_approval: bool = Field(True, json_schema_extra={"example": True})

class CreatePlaybookRequest(BaseModel):
    name: str = Field("Automated Host Isolation", json_schema_extra={"example": "Automated Host Isolation"})
    description: str = Field("Triggers immediate containment upon P1 Critical Threat detection.", json_schema_extra={"example": "Triggers immediate containment upon P1 Critical Threat detection."})
    trigger_type: str = Field("P1_CRITICAL_ALERT", json_schema_extra={"example": "P1_CRITICAL_ALERT"})
    severity_threshold: str = Field("P1_CRITICAL", json_schema_extra={"example": "P1_CRITICAL"})
    requires_approval: bool = Field(True, json_schema_extra={"example": True})
    steps: Optional[List[CreatePlaybookStepRequest]] = None

class ExecutePlaybookRequest(BaseModel):
    playbook_id: str = Field("PB-CONTAIN-HOST", json_schema_extra={"example": "PB-CONTAIN-HOST"})
    target_resource: str = Field("11111111-1111-1111-1111-111111111111", json_schema_extra={"example": "11111111-1111-1111-1111-111111111111"})
    dry_run: bool = Field(False, json_schema_extra={"example": False})
    incident_id: Optional[str] = None

class RejectApprovalRequest(BaseModel):
    rejection_reason: str = Field("Risk too high for host", json_schema_extra={"example": "Risk too high for host"})

class PlaybookStepDTO(BaseModel):
    step_id: str
    action_type: str
    adapter_name: str
    target_param: str
    description: str
    risk_level: str
    requires_approval: bool

class PlaybookDTO(BaseModel):
    playbook_id: str
    organization_id: str
    name: str
    title: str
    description: str
    version: str
    status: str
    trigger_type: str
    trigger_event: str
    severity_threshold: str
    requires_approval: bool
    steps: List[PlaybookStepDTO]
    actions: List[Dict[str, Any]]
    active: bool
    created_at: str

class PlaybookExecutionDTO(BaseModel):
    execution_id: str
    organization_id: str
    playbook_id: str
    playbook_title: str
    target_resource: str
    status: str
    approval_status: str
    action_results: List[Dict[str, Any]]
    executed_by: str
    timestamp: str
    created_at: Optional[str] = None

class ApprovalRequestDTO(BaseModel):
    approval_id: str
    organization_id: str
    execution_id: str
    requested_action: str
    requested_by: str
    approved_by: Optional[str]
    status: str
    requested_at: str

class RollbackRecordDTO(BaseModel):
    rollback_id: str
    execution_id: str
    action_type: str
    rollback_action: str
    status: str
    initiated_by: str
    completed_at: str


# --- PLAYBOOK MANAGEMENT ENDPOINTS ---
@router.post("/api/v1/soar/playbooks", response_model=PlaybookDTO, status_code=201)
async def create_playbook(req: CreatePlaybookRequest, x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Creates a new SOAR response playbook."""
    org_id = x_organization_id or "GLOBAL"
    steps_dict = [s.model_dump() for s in req.steps] if req.steps else None
    pb = await soar_service.create_playbook(
        organization_id=org_id,
        name=req.name,
        description=req.description,
        trigger_type=req.trigger_type,
        severity_threshold=req.severity_threshold,
        requires_approval=req.requires_approval,
        steps=steps_dict
    )
    return PlaybookDTO(
        playbook_id=pb.playbook_id,
        organization_id=pb.organization_id,
        name=pb.name,
        title=pb.title,
        description=pb.description,
        version=pb.version,
        status=pb.status,
        trigger_type=pb.trigger_type,
        trigger_event=pb.trigger_event,
        severity_threshold=pb.severity_threshold,
        requires_approval=pb.requires_approval,
        steps=[PlaybookStepDTO(step_id=s.step_id, action_type=s.action_type, adapter_name=s.adapter_name, target_param=s.target_param, description=s.description, risk_level=s.risk_level, requires_approval=s.requires_approval) for s in pb.steps],
        actions=[{"action_type": a.action_type, "target_param": a.target_param, "description": a.description} for a in pb.actions],
        active=pb.active,
        created_at=pb.created_at.isoformat()
    )

@router.get("/api/v1/soar/playbooks", response_model=List[PlaybookDTO])
async def list_playbooks(x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Lists active SOAR playbooks and action workflows."""
    org_id = x_organization_id or "GLOBAL"
    playbooks = soar_service.list_playbooks(org_id)
    return [
        PlaybookDTO(
            playbook_id=p.playbook_id,
            organization_id=p.organization_id,
            name=p.name,
            title=p.title,
            description=p.description,
            version=p.version,
            status=p.status,
            trigger_type=p.trigger_type,
            trigger_event=p.trigger_event,
            severity_threshold=p.severity_threshold,
            requires_approval=p.requires_approval,
            steps=[PlaybookStepDTO(step_id=s.step_id, action_type=s.action_type, adapter_name=s.adapter_name, target_param=s.target_param, description=s.description, risk_level=s.risk_level, requires_approval=s.requires_approval) for s in p.steps],
            actions=[{"action_type": a.action_type, "target_param": a.target_param, "description": a.description} for a in p.actions],
            active=p.active,
            created_at=p.created_at.isoformat()
        ) for p in playbooks
    ]

@router.get("/api/v1/soar/playbooks/{playbook_id}", response_model=PlaybookDTO)
async def get_playbook(playbook_id: str):
    """Retrieves a single playbook by ID."""
    pb = soar_service.get_playbook(playbook_id)
    if not pb:
        raise HTTPException(status_code=404, detail="Playbook not found.")
    return PlaybookDTO(
        playbook_id=pb.playbook_id,
        organization_id=pb.organization_id,
        name=pb.name,
        title=pb.title,
        description=pb.description,
        version=pb.version,
        status=pb.status,
        trigger_type=pb.trigger_type,
        trigger_event=pb.trigger_event,
        severity_threshold=pb.severity_threshold,
        requires_approval=pb.requires_approval,
        steps=[PlaybookStepDTO(step_id=s.step_id, action_type=s.action_type, adapter_name=s.adapter_name, target_param=s.target_param, description=s.description, risk_level=s.risk_level, requires_approval=s.requires_approval) for s in pb.steps],
        actions=[{"action_type": a.action_type, "target_param": a.target_param, "description": a.description} for a in pb.actions],
        active=pb.active,
        created_at=pb.created_at.isoformat()
    )

@router.post("/api/v1/soar/playbooks/{playbook_id}/activate", response_model=PlaybookDTO)
async def activate_playbook(playbook_id: str):
    """Activates a playbook."""
    pb = await soar_service.activate_playbook(playbook_id)
    if not pb:
        raise HTTPException(status_code=404, detail="Playbook not found.")
    return PlaybookDTO(
        playbook_id=pb.playbook_id, organization_id=pb.organization_id, name=pb.name, title=pb.title, description=pb.description, version=pb.version, status=pb.status, trigger_type=pb.trigger_type, trigger_event=pb.trigger_event, severity_threshold=pb.severity_threshold, requires_approval=pb.requires_approval, steps=[], actions=[], active=pb.active, created_at=pb.created_at.isoformat()
    )

@router.post("/api/v1/soar/playbooks/{playbook_id}/disable", response_model=PlaybookDTO)
async def disable_playbook(playbook_id: str):
    """Disables a playbook."""
    pb = await soar_service.disable_playbook(playbook_id)
    if not pb:
        raise HTTPException(status_code=404, detail="Playbook not found.")
    return PlaybookDTO(
        playbook_id=pb.playbook_id, organization_id=pb.organization_id, name=pb.name, title=pb.title, description=pb.description, version=pb.version, status=pb.status, trigger_type=pb.trigger_type, trigger_event=pb.trigger_event, severity_threshold=pb.severity_threshold, requires_approval=pb.requires_approval, steps=[], actions=[], active=pb.active, created_at=pb.created_at.isoformat()
    )


# --- EXECUTION ENDPOINTS ---
@router.post("/api/v1/soar/executions", response_model=PlaybookExecutionDTO, status_code=201)
async def create_execution(req: ExecutePlaybookRequest, x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Triggers automated response playbook execution."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    try:
        record = await soar_service.execute_playbook(
            playbook_id=req.playbook_id,
            organization_id=org_id,
            target_resource=req.target_resource,
            dry_run=req.dry_run,
            incident_id=req.incident_id
        )
        return PlaybookExecutionDTO(
            execution_id=record.execution_id,
            organization_id=record.organization_id,
            playbook_id=record.playbook_id,
            playbook_title=getattr(record, "playbook_title", record.playbook_id),
            target_resource=record.target_resource,
            status=record.status,
            approval_status=record.approval_status,
            action_results=record.action_results,
            executed_by=record.initiated_by,
            timestamp=record.started_at.isoformat()
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/api/v1/soar/playbooks/execute", response_model=PlaybookExecutionDTO)
async def execute_playbook_legacy(payload: ExecutePlaybookRequest, x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Legacy execution endpoint for backward compatibility."""
    return await create_execution(payload, x_organization_id)

@router.get("/api/v1/soar/executions", response_model=List[PlaybookExecutionDTO])
async def list_executions(x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Returns execution audit history for tenant."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    executions = soar_service.list_executions(org_id)
    return [
        PlaybookExecutionDTO(
            execution_id=e.execution_id,
            organization_id=e.organization_id,
            playbook_id=e.playbook_id,
            playbook_title=getattr(e, "playbook_title", e.playbook_id),
            target_resource=e.target_resource,
            status=e.status,
            approval_status=e.approval_status,
            action_results=e.action_results,
            executed_by=e.initiated_by,
            timestamp=e.started_at.isoformat()
        ) for e in executions
    ]

@router.get("/api/v1/soar/executions/{execution_id}", response_model=PlaybookExecutionDTO)
async def get_execution(execution_id: str):
    """Retrieves single execution details."""
    ex = soar_service.get_execution(execution_id)
    if not ex:
        raise HTTPException(status_code=404, detail="Execution not found.")
    return PlaybookExecutionDTO(
        execution_id=ex.execution_id,
        organization_id=ex.organization_id,
        playbook_id=ex.playbook_id,
        playbook_title=getattr(ex, "playbook_title", ex.playbook_id),
        target_resource=ex.target_resource,
        status=ex.status,
        approval_status=ex.approval_status,
        action_results=ex.action_results,
        executed_by=ex.initiated_by,
        timestamp=ex.started_at.isoformat()
    )

@router.post("/api/v1/soar/executions/{execution_id}/cancel", response_model=PlaybookExecutionDTO)
async def cancel_execution(execution_id: str):
    """Cancels a pending execution."""
    try:
        ex = await soar_service.cancel_execution(execution_id)
        return PlaybookExecutionDTO(execution_id=ex.execution_id, organization_id=ex.organization_id, playbook_id=ex.playbook_id, playbook_title=getattr(ex, "playbook_title", ex.playbook_id), target_resource=ex.target_resource, status=ex.status, approval_status=ex.approval_status, action_results=ex.action_results, executed_by=ex.initiated_by, timestamp=ex.started_at.isoformat())
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/api/v1/soar/executions/{execution_id}/rollback", response_model=RollbackRecordDTO)
async def rollback_execution(execution_id: str):
    """Executes rollback to revert containment actions."""
    try:
        rec = await soar_service.rollback_execution(execution_id)
        return RollbackRecordDTO(
            rollback_id=rec.rollback_id,
            execution_id=rec.execution_id,
            action_type=rec.action_type,
            rollback_action=rec.rollback_action,
            status=rec.status,
            initiated_by=rec.initiated_by,
            completed_at=rec.completed_at.isoformat()
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


# --- APPROVAL ENDPOINTS ---
@router.get("/api/v1/soar/approvals", response_model=List[ApprovalRequestDTO])
async def list_approvals(x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Lists pending human approval requests."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    approvals = soar_service.list_approvals(org_id)
    return [
        ApprovalRequestDTO(
            approval_id=a.approval_id,
            organization_id=a.organization_id,
            execution_id=a.execution_id,
            requested_action=a.requested_action,
            requested_by=a.requested_by,
            approved_by=a.approved_by,
            status=a.status,
            requested_at=a.requested_at.isoformat()
        ) for a in approvals
    ]

@router.post("/api/v1/soar/approvals/{approval_id}/approve", response_model=PlaybookExecutionDTO)
async def approve_request(approval_id: str):
    """Approves a high-risk action execution gate."""
    try:
        record = await soar_service.approve_request(approval_id)
        return PlaybookExecutionDTO(
            execution_id=record.execution_id,
            organization_id=record.organization_id,
            playbook_id=record.playbook_id,
            playbook_title=getattr(record, "playbook_title", record.playbook_id),
            target_resource=record.target_resource,
            status=record.status,
            approval_status=record.approval_status,
            action_results=record.action_results,
            executed_by=record.initiated_by,
            timestamp=record.started_at.isoformat()
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.post("/api/v1/soar/approvals/{approval_id}/reject", response_model=ApprovalRequestDTO)
async def reject_request(approval_id: str, req: RejectApprovalRequest):
    """Rejects a high-risk action execution gate."""
    try:
        a = await soar_service.reject_request(approval_id, req.rejection_reason)
        return ApprovalRequestDTO(
            approval_id=a.approval_id,
            organization_id=a.organization_id,
            execution_id=a.execution_id,
            requested_action=a.requested_action,
            requested_by=a.requested_by,
            approved_by=a.approved_by,
            status=a.status,
            requested_at=a.requested_at.isoformat()
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
