"""
Gestiva Security (GestivaSec V1) — SPRINT 8: Incident & Case Management REST API Router
Exposes comprehensive REST API for Incidents, Cases, Timelines, Evidence, Comments, Escalation, and RCA Closures.
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field

from backend.application.incident_case_service import IncidentCaseApplicationService

router = APIRouter(tags=["Incident & Case Management Lifecycle"])
case_service = IncidentCaseApplicationService()

# --- REQUEST / DTO MODELS ---
class CreateIncidentRequest(BaseModel):
    title: str = Field("P1 Critical Host Compromise Attempt", json_schema_extra={"example": "P1 Critical Host Compromise Attempt"})
    description: str = Field("Multiple brute force auth failures followed by escalation attempt.", json_schema_extra={"example": "Multiple brute force auth failures followed by escalation attempt."})
    origin_type: str = Field("ATTACK_CHAIN", json_schema_extra={"example": "ATTACK_CHAIN"})
    source_reference: str = Field("", json_schema_extra={"example": "CHAIN-883F91A2"})
    severity: str = Field("P1_CRITICAL", json_schema_extra={"example": "P1_CRITICAL"})
    priority: str = Field("P1", json_schema_extra={"example": "P1"})
    category: str = Field("AUTHENTICATION", json_schema_extra={"example": "AUTHENTICATION"})
    asset_id: Optional[str] = None
    target_ip: Optional[str] = Field("192.168.1.100", json_schema_extra={"example": "192.168.1.100"})
    assigned_to: Optional[str] = Field("tier2@gestivaone.com", json_schema_extra={"example": "tier2@gestivaone.com"})

class AssignRequest(BaseModel):
    assigned_to: str = Field("tier2@gestivaone.com", json_schema_extra={"example": "tier2@gestivaone.com"})

class EscalateRequest(BaseModel):
    trigger_reason: str = Field("SLA Breach / Critical Host Escalation", json_schema_extra={"example": "SLA Breach / Critical Host Escalation"})
    escalated_to: str = Field("soc-lead@gestivaone.com", json_schema_extra={"example": "soc-lead@gestivaone.com"})

class ResolveRequest(BaseModel):
    resolution_summary: str = Field("Host contained and malicious session terminated.", json_schema_extra={"example": "Host contained and malicious session terminated."})

class CloseRequest(BaseModel):
    root_cause: str = Field("Weak SSH password allowed brute force compromise.", json_schema_extra={"example": "Weak SSH password allowed brute force compromise."})
    closure_reason: str = Field("Remediation confirmed by SOC Lead.", json_schema_extra={"example": "Remediation confirmed by SOC Lead."})

class AttachEvidenceRequest(BaseModel):
    source_type: str = Field("GES_EVENT", json_schema_extra={"example": "GES_EVENT"})
    source_id: str = Field("evt-123456", json_schema_extra={"example": "evt-123456"})
    description: str = Field("Raw Syslog Authentication Failure Log Payload", json_schema_extra={"example": "Raw Syslog Authentication Failure Log Payload"})
    payload: Dict[str, Any] = Field(default_factory=dict)
    case_id: Optional[str] = None

class AddCommentRequest(BaseModel):
    content: str = Field("Analyst started forensic memory dump analysis.", json_schema_extra={"example": "Analyst started forensic memory dump analysis."})

class CreateCaseRequest(BaseModel):
    title: str = Field("P1 Critical Host Compromise Investigation", json_schema_extra={"example": "P1 Critical Host Compromise Investigation"})
    description: str = Field("Forensic investigation workspace for compromised host.", json_schema_extra={"example": "Forensic investigation workspace for compromised host."})
    severity: str = Field("P1_CRITICAL", json_schema_extra={"example": "P1_CRITICAL"})
    asset_id: Optional[str] = None
    target_ip: Optional[str] = Field("192.168.1.100", json_schema_extra={"example": "192.168.1.100"})
    attack_chain_id: Optional[str] = None
    assigned_analyst_email: Optional[str] = Field("tier2@gestivaone.com", json_schema_extra={"example": "tier2@gestivaone.com"})
    incident_id: Optional[str] = None

class TransitionCaseStatusRequest(BaseModel):
    status: str = Field("CONTAINED", json_schema_extra={"example": "CONTAINED"})
    rca_summary: Optional[str] = Field(None, json_schema_extra={"example": "SSH brute force password list compromised weak admin credential."})
    remediation_actions: Optional[List[str]] = Field(default_factory=list)
    user_email: str = Field("analyst@gestivaone.com", json_schema_extra={"example": "analyst@gestivaone.com"})

class IncidentDTO(BaseModel):
    incident_id: str
    organization_id: str
    incident_number: int
    title: str
    description: str
    source: str
    origin_type: str
    source_reference: str
    severity: str
    priority: str
    status: str
    category: str
    assigned_to: Optional[str]
    assigned_team: Optional[str]
    asset_id: Optional[str]
    target_ip: Optional[str]
    created_at: str
    updated_at: str
    sla_deadline: str

class CaseDTO(BaseModel):
    case_id: str
    organization_id: str
    incident_id: str
    case_number: int
    title: str
    status: str
    priority: str
    assigned_to: Optional[str]
    assigned_team: Optional[str]
    created_at: str
    updated_at: str

# --- INCIDENTS REST ENDPOINTS ---
@router.post("/api/v1/incidents", response_model=IncidentDTO, status_code=201)
async def create_incident(req: CreateIncidentRequest, x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Creates an Incident with deduplication safeguard."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    inc = await case_service.create_incident(
        organization_id=org_id,
        title=req.title,
        description=req.description,
        origin_type=req.origin_type,
        source_reference=req.source_reference,
        severity=req.severity,
        priority=req.priority,
        category=req.category,
        asset_id=req.asset_id,
        target_ip=req.target_ip,
        assigned_to=req.assigned_to
    )
    return IncidentDTO(
        incident_id=inc.incident_id,
        organization_id=inc.organization_id,
        incident_number=inc.incident_number,
        title=inc.title,
        description=inc.description,
        source=inc.source,
        origin_type=inc.origin_type,
        source_reference=inc.source_reference,
        severity=inc.severity,
        priority=inc.priority,
        status=inc.status,
        category=inc.category,
        assigned_to=inc.assigned_to,
        assigned_team=inc.assigned_team,
        asset_id=inc.asset_id,
        target_ip=inc.target_ip,
        created_at=inc.created_at.isoformat(),
        updated_at=inc.updated_at.isoformat(),
        sla_deadline=inc.sla_deadline.isoformat()
    )

@router.get("/api/v1/incidents", response_model=List[IncidentDTO])
async def list_incidents(x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Returns incidents for current tenant."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    incidents = case_service.list_incidents(org_id)
    return [
        IncidentDTO(
            incident_id=inc.incident_id,
            organization_id=inc.organization_id,
            incident_number=inc.incident_number,
            title=inc.title,
            description=inc.description,
            source=inc.source,
            origin_type=inc.origin_type,
            source_reference=inc.source_reference,
            severity=inc.severity,
            priority=inc.priority,
            status=inc.status,
            category=inc.category,
            assigned_to=inc.assigned_to,
            assigned_team=inc.assigned_team,
            asset_id=inc.asset_id,
            target_ip=inc.target_ip,
            created_at=inc.created_at.isoformat(),
            updated_at=inc.updated_at.isoformat(),
            sla_deadline=inc.sla_deadline.isoformat()
        ) for inc in incidents
    ]

@router.get("/api/v1/incidents/{incident_id}", response_model=IncidentDTO)
async def get_incident(incident_id: str):
    """Retrieves a single incident by ID."""
    inc = case_service.get_incident(incident_id)
    if not inc:
        raise HTTPException(status_code=404, detail="Incident not found")
    return IncidentDTO(
        incident_id=inc.incident_id,
        organization_id=inc.organization_id,
        incident_number=inc.incident_number,
        title=inc.title,
        description=inc.description,
        source=inc.source,
        origin_type=inc.origin_type,
        source_reference=inc.source_reference,
        severity=inc.severity,
        priority=inc.priority,
        status=inc.status,
        category=inc.category,
        assigned_to=inc.assigned_to,
        assigned_team=inc.assigned_team,
        asset_id=inc.asset_id,
        target_ip=inc.target_ip,
        created_at=inc.created_at.isoformat(),
        updated_at=inc.updated_at.isoformat(),
        sla_deadline=inc.sla_deadline.isoformat()
    )

@router.post("/api/v1/incidents/{incident_id}/acknowledge", response_model=IncidentDTO)
async def acknowledge_incident(incident_id: str):
    """Acknowledges an incident (NEW -> ACKNOWLEDGED)."""
    try:
        inc = await case_service.transition_incident_status(incident_id, "ACKNOWLEDGED")
        return IncidentDTO(incident_id=inc.incident_id, organization_id=inc.organization_id, incident_number=inc.incident_number, title=inc.title, description=inc.description, source=inc.source, origin_type=inc.origin_type, source_reference=inc.source_reference, severity=inc.severity, priority=inc.priority, status=inc.status, category=inc.category, assigned_to=inc.assigned_to, assigned_team=inc.assigned_team, asset_id=inc.asset_id, target_ip=inc.target_ip, created_at=inc.created_at.isoformat(), updated_at=inc.updated_at.isoformat(), sla_deadline=inc.sla_deadline.isoformat())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/v1/incidents/{incident_id}/triage", response_model=IncidentDTO)
async def triage_incident(incident_id: str):
    """Triages an incident (ACKNOWLEDGED -> TRIAGED)."""
    try:
        inc = await case_service.transition_incident_status(incident_id, "TRIAGED")
        return IncidentDTO(incident_id=inc.incident_id, organization_id=inc.organization_id, incident_number=inc.incident_number, title=inc.title, description=inc.description, source=inc.source, origin_type=inc.origin_type, source_reference=inc.source_reference, severity=inc.severity, priority=inc.priority, status=inc.status, category=inc.category, assigned_to=inc.assigned_to, assigned_team=inc.assigned_team, asset_id=inc.asset_id, target_ip=inc.target_ip, created_at=inc.created_at.isoformat(), updated_at=inc.updated_at.isoformat(), sla_deadline=inc.sla_deadline.isoformat())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/v1/incidents/{incident_id}/assign", response_model=IncidentDTO)
async def assign_incident(incident_id: str, req: AssignRequest):
    """Assigns incident to an analyst."""
    try:
        inc = await case_service.assign_incident(incident_id, req.assigned_to)
        return IncidentDTO(incident_id=inc.incident_id, organization_id=inc.organization_id, incident_number=inc.incident_number, title=inc.title, description=inc.description, source=inc.source, origin_type=inc.origin_type, source_reference=inc.source_reference, severity=inc.severity, priority=inc.priority, status=inc.status, category=inc.category, assigned_to=inc.assigned_to, assigned_team=inc.assigned_team, asset_id=inc.asset_id, target_ip=inc.target_ip, created_at=inc.created_at.isoformat(), updated_at=inc.updated_at.isoformat(), sla_deadline=inc.sla_deadline.isoformat())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/v1/incidents/{incident_id}/escalate")
async def escalate_incident(incident_id: str, req: EscalateRequest):
    """Escalates an incident."""
    try:
        rec = await case_service.escalate_incident(incident_id, req.trigger_reason, req.escalated_to)
        return {"incident_id": incident_id, "escalated_to": rec.escalated_to, "trigger_reason": rec.trigger_reason, "timestamp": rec.timestamp.isoformat()}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/v1/incidents/{incident_id}/resolve", response_model=IncidentDTO)
async def resolve_incident(incident_id: str, req: ResolveRequest):
    """Resolves an incident."""
    try:
        inc = await case_service.transition_incident_status(incident_id, "RESOLVED", resolution_summary=req.resolution_summary)
        return IncidentDTO(incident_id=inc.incident_id, organization_id=inc.organization_id, incident_number=inc.incident_number, title=inc.title, description=inc.description, source=inc.source, origin_type=inc.origin_type, source_reference=inc.source_reference, severity=inc.severity, priority=inc.priority, status=inc.status, category=inc.category, assigned_to=inc.assigned_to, assigned_team=inc.assigned_team, asset_id=inc.asset_id, target_ip=inc.target_ip, created_at=inc.created_at.isoformat(), updated_at=inc.updated_at.isoformat(), sla_deadline=inc.sla_deadline.isoformat())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/v1/incidents/{incident_id}/close", response_model=IncidentDTO)
async def close_incident(incident_id: str, req: CloseRequest):
    """Closes an incident requiring Root Cause Analysis (RCA)."""
    try:
        inc = await case_service.transition_incident_status(incident_id, "CLOSED", root_cause=req.root_cause, closure_reason=req.closure_reason)
        return IncidentDTO(incident_id=inc.incident_id, organization_id=inc.organization_id, incident_number=inc.incident_number, title=inc.title, description=inc.description, source=inc.source, origin_type=inc.origin_type, source_reference=inc.source_reference, severity=inc.severity, priority=inc.priority, status=inc.status, category=inc.category, assigned_to=inc.assigned_to, assigned_team=inc.assigned_team, asset_id=inc.asset_id, target_ip=inc.target_ip, created_at=inc.created_at.isoformat(), updated_at=inc.updated_at.isoformat(), sla_deadline=inc.sla_deadline.isoformat())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

class LegacyTransitionRequest(BaseModel):
    status: str
    rca_report: Optional[str] = None

@router.post("/api/v1/incidents/{incident_id}/transition")
async def transition_incident_legacy(incident_id: str, req: LegacyTransitionRequest):
    """Transitions incident status for backward compatibility."""
    try:
        inc = await case_service.transition_incident_status(incident_id, req.status, root_cause=req.rca_report, closure_reason=req.rca_report)
        return {
            "id": inc.incident_id,
            "alert_id": "alt-001",
            "title": inc.title,
            "severity": inc.severity,
            "status": inc.status,
            "assigned_to": inc.assigned_to or "analyst@gestivaone.com",
            "notes": [t.description for t in case_service.get_incident_timeline(inc.incident_id)],
            "rca_report": inc.root_cause,
            "created_at": inc.created_at.isoformat()
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/api/v1/incidents/{incident_id}/timeline")
async def get_incident_timeline(incident_id: str):
    """Retrieves chronological timeline for an incident."""
    timeline = case_service.get_incident_timeline(incident_id)
    return {"incident_id": incident_id, "timeline": [
        {
            "entry_id": t.entry_id,
            "event_type": t.event_type,
            "description": t.description,
            "actor_id": t.actor_id,
            "timestamp": t.timestamp.isoformat(),
            "previous_state": t.previous_state,
            "new_state": t.new_state
        } for t in timeline
    ]}

@router.get("/api/v1/incidents/{incident_id}/evidence")
async def get_incident_evidence(incident_id: str):
    """Retrieves attached forensic evidence."""
    evidence = case_service.get_incident_evidence(incident_id)
    return {"incident_id": incident_id, "evidence": [
        {
            "evidence_id": e.evidence_id,
            "source_type": e.source_type,
            "source_id": e.source_id,
            "description": e.description,
            "payload": e.payload,
            "added_by": e.added_by,
            "created_at": e.created_at.isoformat(),
            "hash_reference": e.hash_reference
        } for e in evidence
    ]}

@router.post("/api/v1/incidents/{incident_id}/evidence")
async def attach_incident_evidence(incident_id: str, req: AttachEvidenceRequest):
    """Attaches forensic evidence to an incident."""
    ev = await case_service.attach_evidence(
        incident_id=incident_id,
        source_type=req.source_type,
        source_id=req.source_id,
        description=req.description,
        payload=req.payload,
        case_id=req.case_id
    )
    return {
        "evidence_id": ev.evidence_id,
        "incident_id": ev.incident_id,
        "description": ev.description,
        "hash_reference": ev.hash_reference,
        "created_at": ev.created_at.isoformat()
    }

@router.post("/api/v1/incidents/{incident_id}/comments")
async def add_incident_comment(incident_id: str, req: AddCommentRequest, user_email: str = "analyst@gestivaone.com"):
    """Adds analyst comment to an incident."""
    comment = case_service.add_comment(incident_id, user_email, req.content)
    return {
        "comment_id": comment.comment_id,
        "incident_id": comment.incident_id,
        "author_id": comment.author_id,
        "content": comment.content,
        "created_at": comment.created_at.isoformat()
    }

# --- CASES REST ENDPOINTS ---
@router.post("/api/v1/cases", response_model=CaseDTO, status_code=201)
async def create_case(req: CreateCaseRequest, x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Creates a Case workspace."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    c = await case_service.create_case(
        organization_id=org_id,
        title=req.title,
        description=req.description,
        severity=req.severity,
        asset_id=req.asset_id,
        target_ip=req.target_ip,
        attack_chain_id=req.attack_chain_id,
        assigned_analyst_email=req.assigned_analyst_email,
        incident_id=req.incident_id
    )
    return CaseDTO(
        case_id=c.case_id,
        organization_id=c.organization_id,
        incident_id=c.incident_id,
        case_number=c.case_number,
        title=c.title,
        status=c.status,
        priority=c.priority,
        assigned_to=c.assigned_analyst_email,
        assigned_team=c.assigned_team,
        created_at=c.created_at.isoformat(),
        updated_at=c.updated_at.isoformat()
    )

@router.get("/api/v1/cases", response_model=List[CaseDTO])
async def list_cases(x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Returns cases for current tenant."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    cases = await case_service.list_cases(org_id)
    return [
        CaseDTO(
            case_id=c.case_id,
            organization_id=c.organization_id,
            incident_id=c.incident_id,
            case_number=c.case_number,
            title=c.title,
            status=c.status,
            priority=c.priority,
            assigned_to=c.assigned_analyst_email,
            assigned_team=c.assigned_team,
            created_at=c.created_at.isoformat(),
            updated_at=c.updated_at.isoformat()
        ) for c in cases
    ]

@router.get("/api/v1/cases/{case_id}", response_model=CaseDTO)
async def get_case(case_id: str):
    """Retrieves a single case by ID."""
    c = case_service.get_case(case_id)
    if not c:
        raise HTTPException(status_code=404, detail="Case not found")
    return CaseDTO(
        case_id=c.case_id,
        organization_id=c.organization_id,
        incident_id=c.incident_id,
        case_number=c.case_number,
        title=c.title,
        status=c.status,
        priority=c.priority,
        assigned_to=c.assigned_analyst_email,
        assigned_team=c.assigned_team,
        created_at=c.created_at.isoformat(),
        updated_at=c.updated_at.isoformat()
    )

@router.patch("/api/v1/cases/{case_id}", response_model=CaseDTO)
async def update_case_status_patch(case_id: str, req: TransitionCaseStatusRequest):
    """Updates case status via PATCH."""
    try:
        c = await case_service.transition_case_status(case_id, req.status, user_email=req.user_email, rca_summary=req.rca_summary, remediation_actions=req.remediation_actions)
        return CaseDTO(case_id=c.case_id, organization_id=c.organization_id, incident_id=c.incident_id, case_number=c.case_number, title=c.title, status=c.status, priority=c.priority, assigned_to=c.assigned_to, assigned_team=c.assigned_team, created_at=c.created_at.isoformat(), updated_at=c.updated_at.isoformat())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/v1/cases/{case_id}/assign", response_model=CaseDTO)
async def assign_case(case_id: str, req: AssignRequest):
    """Assigns case to an analyst."""
    c = case_service.get_case(case_id)
    if not c:
        raise HTTPException(status_code=404, detail="Case not found")
    c.assigned_analyst_email = req.assigned_to
    c.assigned_to = req.assigned_to
    c.updated_at = datetime.now(timezone.utc)
    return CaseDTO(case_id=c.case_id, organization_id=c.organization_id, incident_id=c.incident_id, case_number=c.case_number, title=c.title, status=c.status, priority=c.priority, assigned_to=c.assigned_to, assigned_team=c.assigned_team, created_at=c.created_at.isoformat(), updated_at=c.updated_at.isoformat())

@router.post("/api/v1/cases/{case_id}/resolve", response_model=CaseDTO)
async def resolve_case(case_id: str):
    """Resolves a case."""
    try:
        c = await case_service.transition_case_status(case_id, "RESOLVED")
        return CaseDTO(case_id=c.case_id, organization_id=c.organization_id, incident_id=c.incident_id, case_number=c.case_number, title=c.title, status=c.status, priority=c.priority, assigned_to=c.assigned_to, assigned_team=c.assigned_team, created_at=c.created_at.isoformat(), updated_at=c.updated_at.isoformat())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/api/v1/cases/{case_id}/close", response_model=CaseDTO)
async def close_case(case_id: str, req: TransitionCaseStatusRequest):
    """Closes a case with RCA summary."""
    try:
        c = await case_service.transition_case_status(case_id, "CLOSED", user_email=req.user_email, rca_summary=req.rca_summary, remediation_actions=req.remediation_actions)
        return CaseDTO(case_id=c.case_id, organization_id=c.organization_id, incident_id=c.incident_id, case_number=c.case_number, title=c.title, status=c.status, priority=c.priority, assigned_to=c.assigned_to, assigned_team=c.assigned_team, created_at=c.created_at.isoformat(), updated_at=c.updated_at.isoformat())
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# --- BACKWARD COMPATIBILITY ENDPOINTS (/api/v1/incidents/cases) ---
@router.post("/api/v1/incidents/cases", response_model=CaseDTO, status_code=201)
async def create_incident_case_legacy(payload: CreateCaseRequest, x_organization_id: Optional[str] = Header(None)):
    return await create_case(payload, x_organization_id)

@router.get("/api/v1/incidents/cases", response_model=List[CaseDTO])
async def list_incident_cases_legacy(x_organization_id: Optional[str] = Header(None)):
    return await list_cases(x_organization_id)
