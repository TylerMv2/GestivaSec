"""
Gestiva Security (GestivaSec V1) — SPRINT 10: SOAR Engine Application Service
Orchestrates Playbook Execution, Human Approval Gates, Safety Risk Models, Integration Adapters, Rollback, and Audit Trail.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from backend.domain.soar_playbook import (
    Playbook,
    PlaybookStep,
    PlaybookExecution,
    PlaybookExecutionStep,
    PlaybookExecutionRecord,
    ApprovalRequest,
    RollbackRecord,
    ActionRiskLevel,
    PlaybookStatus,
    ExecutionStatus,
    ApprovalStatus,
    ALLOWED_ACTION_TYPES
)
from backend.infrastructure.playbook_registry import PlaybookRegistry
from backend.infrastructure.containment_adapters import ContainmentActionAdapters
from backend.infrastructure.audit_repository import AuditRepository, AuditEvent

_EXECUTION_HISTORY_STORE: List[PlaybookExecution] = []
_APPROVAL_REQUESTS_STORE: List[ApprovalRequest] = []
_ROLLBACK_RECORDS_STORE: List[RollbackRecord] = []

class SoarApplicationService:
    def __init__(
        self,
        registry: Optional[PlaybookRegistry] = None,
        adapters: Optional[ContainmentActionAdapters] = None,
        audit_repo: Optional[AuditRepository] = None
    ):
        self.registry = registry or PlaybookRegistry()
        self.adapters = adapters or ContainmentActionAdapters()
        self.audit_repo = audit_repo or AuditRepository()

    # --- PLAYBOOK MANAGEMENT ---
    async def create_playbook(
        self,
        organization_id: str,
        name: str,
        description: str,
        trigger_type: str = "P1_CRITICAL_ALERT",
        severity_threshold: str = "P1_CRITICAL",
        requires_approval: bool = True,
        steps: Optional[List[Dict[str, Any]]] = None,
        created_by: str = "soc-admin@gestivaone.com"
    ) -> Playbook:
        parsed_steps = []
        if steps:
            for s in steps:
                act = s.get("action_type", "ISOLATE_HOST")
                if act not in ALLOWED_ACTION_TYPES:
                    raise ValueError(f"Action type {act} is not allowed.")
                parsed_steps.append(
                    PlaybookStep(
                        action_type=act,
                        adapter_name=s.get("adapter_name", "MockEDRAdapter"),
                        target_param=s.get("target_param", "asset_id"),
                        description=s.get("description", "Automated step action"),
                        risk_level=s.get("risk_level", ActionRiskLevel.HIGH),
                        requires_approval=s.get("requires_approval", True)
                    )
                )

        pb = Playbook(
            organization_id=organization_id,
            name=name,
            title=name,
            description=description,
            trigger_type=trigger_type,
            trigger_event=trigger_type,
            severity_threshold=severity_threshold,
            requires_approval=requires_approval,
            steps=parsed_steps,
            created_by=created_by,
            updated_by=created_by
        )
        added = self.registry.add_playbook(pb)
        await self.audit_repo.record_event(
            AuditEvent(
                actor_email=created_by,
                organization_id=organization_id,
                action="PLAYBOOK_CREATED",
                resource_type="SOAR_PLAYBOOK",
                resource_id=added.playbook_id,
                details={"name": name, "trigger_type": trigger_type}
            )
        )
        return added

    def list_playbooks(self, organization_id: str = "GLOBAL") -> List[Playbook]:
        return self.registry.list_playbooks(organization_id)

    def get_playbook(self, playbook_id: str) -> Optional[Playbook]:
        return self.registry.get_playbook_by_id(playbook_id)

    async def activate_playbook(self, playbook_id: str, actor_email: str = "soc-admin@gestivaone.com") -> Optional[Playbook]:
        pb = self.registry.set_status(playbook_id, PlaybookStatus.ACTIVE)
        if pb:
            await self.audit_repo.record_event(AuditEvent(actor_email=actor_email, organization_id=pb.organization_id, action="PLAYBOOK_ACTIVATED", resource_type="SOAR_PLAYBOOK", resource_id=pb.playbook_id, details={"status": "ACTIVE"}))
        return pb

    async def disable_playbook(self, playbook_id: str, actor_email: str = "soc-admin@gestivaone.com") -> Optional[Playbook]:
        pb = self.registry.set_status(playbook_id, PlaybookStatus.DISABLED)
        if pb:
            await self.audit_repo.record_event(AuditEvent(actor_email=actor_email, organization_id=pb.organization_id, action="PLAYBOOK_DISABLED", resource_type="SOAR_PLAYBOOK", resource_id=pb.playbook_id, details={"status": "DISABLED"}))
        return pb

    # --- EXECUTION ENGINE ---
    async def execute_playbook(
        self,
        playbook_id: str,
        organization_id: str,
        target_resource: str,
        dry_run: bool = False,
        initiated_by: str = "SOAR_AUTOMATION_ENGINE",
        incident_id: Optional[str] = None,
        case_id: Optional[str] = None
    ) -> PlaybookExecution:
        pb = self.get_playbook(playbook_id)
        if not pb:
            raise ValueError(f"Playbook {playbook_id} not found.")

        # Require approval if playbook requires approval or has HIGH/CRITICAL steps, unless dry_run
        needs_approval = (pb.requires_approval or any(s.risk_level in [ActionRiskLevel.HIGH, ActionRiskLevel.CRITICAL] for s in pb.steps)) and not dry_run

        exec_rec = PlaybookExecution(
            organization_id=organization_id,
            playbook_id=pb.playbook_id,
            playbook_version=pb.version,
            incident_id=incident_id,
            case_id=case_id,
            target_resource=target_resource,
            status=ExecutionStatus.APPROVAL_REQUIRED if needs_approval else (ExecutionStatus.SIMULATED if dry_run else ExecutionStatus.RUNNING),
            initiated_by=initiated_by,
            approval_status=ApprovalStatus.PENDING if needs_approval else ApprovalStatus.APPROVED
        )
        # Compatibility attribute
        setattr(exec_rec, "playbook_title", pb.title)
        setattr(exec_rec, "executed_by", initiated_by)

        _EXECUTION_HISTORY_STORE.append(exec_rec)

        if needs_approval:
            app_req = ApprovalRequest(
                organization_id=organization_id,
                execution_id=exec_rec.execution_id,
                requested_action=pb.steps[0].action_type if pb.steps else "PLAYBOOK_EXECUTION",
                requested_by=initiated_by
            )
            _APPROVAL_REQUESTS_STORE.append(app_req)
            await self.audit_repo.record_event(AuditEvent(actor_email=initiated_by, organization_id=organization_id, action="APPROVAL_REQUESTED", resource_type="SOAR_EXECUTION", resource_id=exec_rec.execution_id, details={"approval_id": app_req.approval_id}))
            return exec_rec

        # Execute Actions
        return await self._run_execution_steps(exec_rec, pb, target_resource, dry_run=dry_run, initiated_by=initiated_by)

    async def _run_execution_steps(self, exec_rec: PlaybookExecution, pb: Playbook, target_resource: str, dry_run: bool, initiated_by: str) -> PlaybookExecution:
        action_results = []
        
        # Backward compatibility for default playbooks
        if not pb.steps and pb.actions:
            for action in pb.actions:
                act_type = getattr(action, "action_type", "ISOLATE_ASSET")
                if act_type in ["ISOLATE_ASSET", "ISOLATE_HOST"]:
                    res = self.adapters.isolate_asset(target_resource, dry_run=dry_run)
                elif act_type in ["BLOCK_FIREWALL_IP", "BLOCK_IP"]:
                    res = self.adapters.block_firewall_ip(target_resource, dry_run=dry_run)
                elif act_type in ["DISPATCH_NOTIFICATION", "NOTIFY_ANALYST"]:
                    res = self.adapters.dispatch_notification(target_resource, {"playbook": pb.title}, dry_run=dry_run)
                else:
                    res = {"action": act_type, "target": target_resource, "status": "COMPLETED" if not dry_run else "SIMULATED"}
                action_results.append(res)
        else:
            for step in pb.steps:
                now = datetime.now(timezone.utc)
                if step.action_type in ["ISOLATE_HOST", "ISOLATE_ASSET"]:
                    res = self.adapters.isolate_asset(target_resource, dry_run=dry_run)
                elif step.action_type in ["BLOCK_IP", "BLOCK_FIREWALL_IP"]:
                    res = self.adapters.block_firewall_ip(target_resource, dry_run=dry_run)
                elif step.action_type in ["NOTIFY_ANALYST", "DISPATCH_NOTIFICATION", "NOTIFY_SOC_LEAD"]:
                    res = self.adapters.dispatch_notification(target_resource, {"playbook": pb.name}, dry_run=dry_run)
                else:
                    res = {"action": step.action_type, "target": target_resource, "status": "COMPLETED" if not dry_run else "SIMULATED"}
                action_results.append(res)

                exec_step = PlaybookExecutionStep(
                    execution_id=exec_rec.execution_id,
                    step_id=step.step_id,
                    action_type=step.action_type,
                    adapter=step.adapter_name,
                    status="SUCCESS" if not dry_run else "SIMULATED",
                    completed_at=now,
                    response_reference=res
                )
                exec_rec.executed_steps.append(exec_step)

        exec_rec.action_results = action_results
        exec_rec.status = "SIMULATED" if dry_run else ExecutionStatus.COMPLETED
        exec_rec.completed_at = datetime.now(timezone.utc)

        await self.audit_repo.record_event(
            AuditEvent(
                actor_email=initiated_by,
                organization_id=exec_rec.organization_id,
                action="PLAYBOOK_EXECUTED",
                resource_type="SOAR_PLAYBOOK",
                resource_id=pb.playbook_id,
                details={"execution_id": exec_rec.execution_id, "dry_run": dry_run, "status": exec_rec.status}
            )
        )
        return exec_rec

    def get_execution(self, execution_id: str) -> Optional[PlaybookExecution]:
        for e in _EXECUTION_HISTORY_STORE:
            if e.execution_id == execution_id: return e
        return None

    def list_executions(self, organization_id: str, limit: int = 50) -> List[PlaybookExecution]:
        return [e for e in _EXECUTION_HISTORY_STORE if e.organization_id == organization_id][-limit:]

    async def cancel_execution(self, execution_id: str, actor_email: str = "soc-admin@gestivaone.com") -> PlaybookExecution:
        ex = self.get_execution(execution_id)
        if not ex: raise ValueError(f"Execution {execution_id} not found.")
        ex.status = ExecutionStatus.CANCELLED
        await self.audit_repo.record_event(AuditEvent(actor_email=actor_email, organization_id=ex.organization_id, action="PLAYBOOK_EXECUTION_CANCELLED", resource_type="SOAR_EXECUTION", resource_id=execution_id, details={"status": "CANCELLED"}))
        return ex

    # --- APPROVALS ---
    def list_approvals(self, organization_id: str) -> List[ApprovalRequest]:
        return [a for a in _APPROVAL_REQUESTS_STORE if a.organization_id == organization_id]

    async def approve_request(self, approval_id: str, approver_email: str = "soc-lead@gestivaone.com") -> PlaybookExecution:
        app_req = next((a for a in _APPROVAL_REQUESTS_STORE if a.approval_id == approval_id), None)
        if not app_req: raise ValueError(f"Approval request {approval_id} not found.")
        app_req.status = ApprovalStatus.APPROVED
        app_req.approved_by = approver_email
        app_req.resolved_at = datetime.now(timezone.utc)

        ex = self.get_execution(app_req.execution_id)
        if not ex: raise ValueError(f"Associated execution {app_req.execution_id} not found.")
        pb = self.get_playbook(ex.playbook_id)

        await self.audit_repo.record_event(AuditEvent(actor_email=approver_email, organization_id=ex.organization_id, action="APPROVAL_GRANTED", resource_type="SOAR_APPROVAL", resource_id=approval_id, details={"execution_id": ex.execution_id}))

        return await self._run_execution_steps(ex, pb, ex.target_resource, dry_run=False, initiated_by=approver_email)

    async def reject_request(self, approval_id: str, rejection_reason: str = "Risk too high", approver_email: str = "soc-lead@gestivaone.com") -> ApprovalRequest:
        app_req = next((a for a in _APPROVAL_REQUESTS_STORE if a.approval_id == approval_id), None)
        if not app_req: raise ValueError(f"Approval request {approval_id} not found.")
        app_req.status = ApprovalStatus.REJECTED
        app_req.approved_by = approver_email
        app_req.rejection_reason = rejection_reason
        app_req.resolved_at = datetime.now(timezone.utc)

        ex = self.get_execution(app_req.execution_id)
        if ex: ex.status = ExecutionStatus.CANCELLED

        await self.audit_repo.record_event(AuditEvent(actor_email=approver_email, organization_id=app_req.organization_id, action="APPROVAL_REJECTED", resource_type="SOAR_APPROVAL", resource_id=approval_id, details={"rejection_reason": rejection_reason}))
        return app_req

    # --- ROLLBACK ---
    async def rollback_execution(self, execution_id: str, actor_email: str = "soc-admin@gestivaone.com") -> RollbackRecord:
        ex = self.get_execution(execution_id)
        if not ex: raise ValueError(f"Execution {execution_id} not found.")

        # Rollback actions
        for result in ex.action_results:
            act = result.get("action")
            if act in ["ISOLATE_ASSET", "ISOLATE_HOST"]:
                self.adapters.edr.rollback(ex.target_resource)
            elif act in ["BLOCK_FIREWALL_IP", "BLOCK_IP"]:
                self.adapters.firewall.rollback(ex.target_resource)

        ex.status = ExecutionStatus.ROLLED_BACK
        ex.rollback_status = "COMPLETED"

        rec = RollbackRecord(
            execution_id=execution_id,
            action_type="ROLLBACK_ALL",
            rollback_action="REVERT_PLAYBOOK_ACTIONS",
            initiated_by=actor_email
        )
        _ROLLBACK_RECORDS_STORE.append(rec)

        await self.audit_repo.record_event(AuditEvent(actor_email=actor_email, organization_id=ex.organization_id, action="ROLLBACK_COMPLETED", resource_type="SOAR_EXECUTION", resource_id=execution_id, details={"rollback_id": rec.rollback_id}))
        return rec
