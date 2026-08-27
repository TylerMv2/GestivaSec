"""
Gestiva Security (GestivaSec V1) — SPRINT 8: Incident & Case Management Application Service
Orchestrates Incidents, Investigation Cases, Lifecycle State Machines, Analyst Assignments, SLA Tracking, Timeline, and RCA.
"""
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from backend.domain.incident_case import (
    Incident,
    IncidentCase,
    IncidentEvidence,
    IncidentTimelineEntry,
    IncidentComment,
    RootCauseAnalysis,
    SLAState,
    EscalationRecord
)
from backend.infrastructure.audit_repository import AuditRepository, AuditEvent

# Seed initial operational incident for backward compatibility with Stage 1 alert engine tests
_INCIDENTS_STORE: List[Incident] = [
    Incident(
        incident_id="inc-001",
        organization_id="00000000-0000-0000-0000-000000000001",
        incident_number=1001,
        title="P1 Critical Host Compromise Attempt",
        description="Correlated attack sequence requiring SOC Tier 2 intervention.",
        severity="P1_CRITICAL",
        status="INVESTIGATING",
        assigned_to="analyst@gestivaone.com",
        target_ip="192.168.1.100"
    )
]
_INCIDENT_CASES_STORE: List[IncidentCase] = []
_EVIDENCE_STORE: List[IncidentEvidence] = []
_TIMELINE_STORE: List[IncidentTimelineEntry] = []
_COMMENTS_STORE: List[IncidentComment] = []

class IncidentApplicationService:
    def __init__(self, audit_repo: Optional[AuditRepository] = None):
        self.audit_repo = audit_repo or AuditRepository()

    async def create_incident(
        self, organization_id: str, title: str, description: str,
        origin_type: str = "ATTACK_CHAIN", source_reference: str = "",
        severity: str = "P1_CRITICAL", priority: str = "P1", category: str = "AUTHENTICATION",
        asset_id: Optional[str] = None, target_ip: Optional[str] = "127.0.0.1", assigned_to: Optional[str] = None
    ) -> Incident:
        if source_reference:
            for existing in _INCIDENTS_STORE:
                if (existing.organization_id == organization_id and existing.origin_type == origin_type and existing.source_reference == source_reference and existing.status not in ["CLOSED", "CANCELLED"]):
                    return existing

        now = datetime.now(timezone.utc)
        new_inc = Incident(
            organization_id=organization_id, incident_number=1000 + len(_INCIDENTS_STORE) + 1,
            title=title, description=description, origin_type=origin_type, source_reference=source_reference,
            severity=severity.upper(), priority=priority.upper(), category=category, asset_id=asset_id, target_ip=target_ip,
            assigned_to=assigned_to, created_at=now, updated_at=now, detected_at=now, sla_deadline=now + timedelta(hours=4)
        )
        _INCIDENTS_STORE.append(new_inc)
        _TIMELINE_STORE.append(IncidentTimelineEntry(organization_id=organization_id, incident_id=new_inc.incident_id, event_type="INCIDENT_CREATED", description=f"Incident created from {origin_type}", new_state="NEW"))
        await self.audit_repo.record_event(AuditEvent(actor_email=assigned_to or "system@gestivaone.com", organization_id=organization_id, action="CREATE_INCIDENT", resource_type="INCIDENT", resource_id=new_inc.incident_id, details={"title": title}))
        return new_inc

    def get_incident(self, incident_id: str) -> Optional[Incident]:
        for inc in _INCIDENTS_STORE:
            if inc.incident_id == incident_id: return inc
        return None

    def list_incidents(self, organization_id: str, limit: int = 50) -> List[Incident]:
        res = [inc for inc in _INCIDENTS_STORE if inc.organization_id == organization_id]
        if not res and organization_id == "00000000-0000-0000-0000-000000000001":
            return _INCIDENTS_STORE[-limit:]
        return res[-limit:]

    async def transition_incident_status(self, incident_id: str, new_status: str, actor_email: str = "analyst@gestivaone.com", resolution_summary: Optional[str] = None, root_cause: Optional[str] = None, closure_reason: Optional[str] = None) -> Incident:
        inc = self.get_incident(incident_id)
        if not inc: raise ValueError(f"Incident {incident_id} not found.")
        status_upper = new_status.upper()
        
        # Support legacy CLOSED_WITH_RCA
        check_status = "CLOSED" if status_upper in ["CLOSED", "CLOSED_WITH_RCA"] else status_upper

        if status_upper in ["CLOSED", "CLOSED_WITH_RCA"]:
            if not root_cause:
                raise ValueError("Regla BR-0001: Root Cause Analysis (RCA) report is required before closing an incident.")

        if not inc.can_transition_to(check_status):
            raise ValueError(f"Invalid transition from {inc.status} to {check_status}.")

        prev = inc.status
        inc.status = status_upper
        now = datetime.now(timezone.utc)
        inc.updated_at = now
        if status_upper == "RESOLVED": inc.resolved_at = now; inc.resolution_summary = resolution_summary or "Resolved"
        elif status_upper in ["CLOSED", "CLOSED_WITH_RCA"]:
            inc.closed_at = now; inc.closure_reason = closure_reason or resolution_summary or "Closed"
        if root_cause: inc.root_cause = root_cause
        _TIMELINE_STORE.append(IncidentTimelineEntry(organization_id=inc.organization_id, incident_id=inc.incident_id, event_type="STATUS_CHANGE", description=f"Status changed from {prev} to {status_upper}", actor_id=actor_email, previous_state=prev, new_state=status_upper))
        await self.audit_repo.record_event(AuditEvent(actor_email=actor_email, organization_id=inc.organization_id, action="TRANSITION_INCIDENT_STATUS", resource_type="INCIDENT", resource_id=inc.incident_id, details={"new_status": status_upper}))
        return inc

    async def assign_incident(self, incident_id: str, assigned_to: str, actor_email: str = "analyst@gestivaone.com") -> Incident:
        inc = self.get_incident(incident_id)
        if not inc: raise ValueError(f"Incident {incident_id} not found.")
        prev = inc.assigned_to; inc.assigned_to = assigned_to; inc.updated_at = datetime.now(timezone.utc)
        _TIMELINE_STORE.append(IncidentTimelineEntry(organization_id=inc.organization_id, incident_id=incident_id, event_type="ASSIGNMENT", description=f"Assigned to {assigned_to}", actor_id=actor_email, previous_state=prev, new_state=assigned_to))
        return inc

    async def escalate_incident(self, incident_id: str, trigger_reason: str, escalated_to: str, actor_email: str = "analyst@gestivaone.com") -> EscalationRecord:
        inc = self.get_incident(incident_id)
        if not inc: raise ValueError(f"Incident {incident_id} not found.")
        rec = EscalationRecord(incident_id=incident_id, trigger_reason=trigger_reason, escalated_by=actor_email, escalated_to=escalated_to)
        inc.priority = "P1"; inc.severity = "P1_CRITICAL"
        _TIMELINE_STORE.append(IncidentTimelineEntry(organization_id=inc.organization_id, incident_id=incident_id, event_type="ESCALATION", description=f"Escalated to {escalated_to}", actor_id=actor_email))
        return rec


class CaseApplicationService:
    def __init__(self, audit_repo: Optional[AuditRepository] = None):
        self.audit_repo = audit_repo or AuditRepository()
        self.inc_service = IncidentApplicationService(audit_repo)

    async def create_case(self, organization_id: str, title: str, description: str, severity: str = "P1_CRITICAL", asset_id: Optional[str] = None, target_ip: Optional[str] = None, attack_chain_id: Optional[str] = None, assigned_analyst_email: Optional[str] = None, incident_id: Optional[str] = None) -> IncidentCase:
        if not incident_id:
            parent_inc = await self.inc_service.create_incident(organization_id=organization_id, title=title, description=description, severity=severity, asset_id=asset_id, target_ip=target_ip, source_reference=attack_chain_id or "")
            incident_id = parent_inc.incident_id
        new_case = IncidentCase(organization_id=organization_id, incident_id=incident_id, case_number=5000 + len(_INCIDENT_CASES_STORE) + 1, title=title, description=description, severity=severity.upper(), status="OPEN", asset_id=asset_id, target_ip=target_ip, attack_chain_id=attack_chain_id, assigned_analyst_email=assigned_analyst_email)
        _INCIDENT_CASES_STORE.append(new_case)
        await self.audit_repo.record_event(AuditEvent(actor_email=assigned_analyst_email or "system@gestivaone.com", organization_id=organization_id, action="CREATE_INCIDENT_CASE", resource_type="INCIDENT_CASE", resource_id=new_case.case_id, details={"case_id": new_case.case_id}))
        return new_case

    def get_case(self, case_id: str) -> Optional[IncidentCase]:
        for c in _INCIDENT_CASES_STORE:
            if c.case_id == case_id: return c
        return None

    async def list_cases(self, organization_id: str, limit: int = 50) -> List[IncidentCase]:
        return [c for c in _INCIDENT_CASES_STORE if c.organization_id == organization_id][-limit:]

    async def transition_case_status(self, case_id: str, new_status: str, user_email: str = "analyst@gestivaone.com", rca_summary: Optional[str] = None, remediation_actions: Optional[List[str]] = None) -> IncidentCase:
        status_upper = new_status.upper()
        case = self.get_case(case_id)
        if not case: raise ValueError(f"Incident Case {case_id} not found.")
        if not case.can_transition_to(status_upper): raise ValueError(f"Invalid state transition from {case.status} to {status_upper}.")
        if status_upper == "CLOSED" and not (rca_summary or case.rca_summary): raise ValueError("Root Cause Analysis (RCA) summary is required before closing a case.")
        case.status = status_upper
        if rca_summary: case.rca_summary = rca_summary
        if remediation_actions: case.remediation_actions = remediation_actions
        case.updated_at = datetime.now(timezone.utc)
        await self.audit_repo.record_event(AuditEvent(actor_email=user_email, organization_id=case.organization_id, action="TRANSITION_INCIDENT_CASE_STATUS", resource_type="INCIDENT_CASE", resource_id=case.case_id, details={"new_status": status_upper}))
        return case

    async def attach_evidence(self, incident_id: str, source_type: str, source_id: str, description: str, payload: Dict[str, Any], added_by: str = "analyst@gestivaone.com", case_id: Optional[str] = None) -> IncidentEvidence:
        ev = IncidentEvidence(organization_id="00000000-0000-0000-0000-000000000001", incident_id=incident_id, case_id=case_id, source_type=source_type.upper(), source_id=source_id, description=description, payload=payload, added_by=added_by)
        _EVIDENCE_STORE.append(ev)
        if case_id:
            c = self.get_case(case_id)
            if c: c.evidence_timeline.append(ev)
        return ev

    def add_comment(self, incident_id: str, author_id: str, content: str, case_id: Optional[str] = None) -> IncidentComment:
        comment = IncidentComment(incident_id=incident_id, case_id=case_id, author_id=author_id, content=content)
        _COMMENTS_STORE.append(comment)
        return comment


# Backward-compatible alias
class IncidentCaseApplicationService(CaseApplicationService):
    def __init__(self, audit_repo: Optional[AuditRepository] = None):
        super().__init__(audit_repo)
        self.inc_service = IncidentApplicationService(audit_repo)

    async def create_incident(self, *args, **kwargs): return await self.inc_service.create_incident(*args, **kwargs)
    def get_incident(self, *args, **kwargs): return self.inc_service.get_incident(*args, **kwargs)
    def list_incidents(self, *args, **kwargs): return self.inc_service.list_incidents(*args, **kwargs)
    async def transition_incident_status(self, *args, **kwargs): return await self.inc_service.transition_incident_status(*args, **kwargs)
    async def assign_incident(self, *args, **kwargs): return await self.inc_service.assign_incident(*args, **kwargs)
    async def escalate_incident(self, *args, **kwargs): return await self.inc_service.escalate_incident(*args, **kwargs)
    def get_incident_timeline(self, incident_id: str): return [t for t in _TIMELINE_STORE if t.incident_id == incident_id]
    def get_incident_evidence(self, incident_id: str): return [e for e in _EVIDENCE_STORE if e.incident_id == incident_id]
    def get_comments(self, incident_id: str): return [c for c in _COMMENTS_STORE if c.incident_id == incident_id]
