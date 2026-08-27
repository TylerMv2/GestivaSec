"""
Gestiva Security (GestivaSec V1) — SPRINT 6: Detection Engine & Alerts REST API Router
Exposes comprehensive REST API for Detection Rules, Event Evaluation, Findings, and Actionable Alert Operations.
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field

from backend.application.detection_service import DetectionEngineService
from backend.domain.detection_rule import DetectionRule, DetectionRuleCondition
from backend.domain.normalized_event import NormalizedEvent, EventSource, EventDestination, EventClassification

router = APIRouter(prefix="/api/v1/detection", tags=["Detection Engine & Alerts Pipeline"])
detection_service = DetectionEngineService()

class RuleConditionDTO(BaseModel):
    field_path: str = "event.action"
    operator: str = "EQUALS"
    target_value: Any = "LOGIN_FAILED"
    threshold_count: int = 1
    time_window_seconds: int = 60

class CreateRuleRequest(BaseModel):
    rule_id: Optional[str] = None
    title: str
    description: str
    severity: str = "P1_CRITICAL"
    category: str = "AUTHENTICATION"
    mitre_attack_id: str = "T1110.001"
    condition: RuleConditionDTO = Field(default_factory=RuleConditionDTO)
    active: bool = True

class UpdateRuleRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    severity: Optional[str] = None
    active: Optional[bool] = None

class RuleDTO(BaseModel):
    rule_id: str
    title: str
    description: str
    severity: str
    category: str
    mitre_attack_id: str
    active: bool

class FindingDTO(BaseModel):
    finding_id: str
    organization_id: str
    rule_id: str
    rule_title: str
    severity: str
    asset_id: Optional[str]
    source_ip: str
    matched_event_ids: List[str]
    confidence_score: float

class ActionableAlertDTO(BaseModel):
    alert_id: str
    organization_id: str
    rule_id: str
    title: str
    severity: str
    asset_id: Optional[str]
    source_ip: str
    status: str
    mitre_attack_id: str
    findings_count: int
    first_seen: str
    last_seen: str

class UpdateAlertStatusRequest(BaseModel):
    status: str = Field("IN_PROGRESS", json_schema_extra={"example": "IN_PROGRESS"})

class AssignAlertRequest(BaseModel):
    assigned_analyst: str = "analyst@gestivaone.com"

class TestRuleRequest(BaseModel):
    rule: CreateRuleRequest
    sample_event: Dict[str, Any]

class EvaluateEventRequest(BaseModel):
    organization_id: str = "00000000-0000-0000-0000-000000000001"
    event_type: str = "AUTHENTICATION"
    action: str = "LOGIN_FAILED"
    source_ip: str = "192.168.1.50"
    asset_id: Optional[str] = "22222222-2222-2222-2222-222222222222"

# 1. RULES ENDPOINTS
@router.get("/rules", response_model=List[RuleDTO])
async def list_detection_rules(include_inactive: bool = False):
    """Lists detection rules and MITRE ATT&CK mappings."""
    rules = detection_service.registry.list_rules(include_inactive=include_inactive)
    return [
        RuleDTO(
            rule_id=r.rule_id,
            title=r.title,
            description=r.description,
            severity=r.severity,
            category=r.category,
            mitre_attack_id=r.mitre_attack_id,
            active=r.active
        ) for r in rules
    ]

@router.get("/rules/{rule_id}", response_model=RuleDTO)
async def get_rule(rule_id: str):
    """Retrieves a single detection rule by ID."""
    rule = detection_service.registry.get_rule_by_id(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return RuleDTO(
        rule_id=rule.rule_id,
        title=rule.title,
        description=rule.description,
        severity=rule.severity,
        category=rule.category,
        mitre_attack_id=rule.mitre_attack_id,
        active=rule.active
    )

@router.post("/rules", response_model=RuleDTO, status_code=201)
async def create_rule(req: CreateRuleRequest):
    """Registers a new detection rule."""
    cond = DetectionRuleCondition(
        field_path=req.condition.field_path,
        operator=req.condition.operator,
        target_value=req.condition.target_value,
        threshold_count=req.condition.threshold_count,
        time_window_seconds=req.condition.time_window_seconds
    )
    new_rule = DetectionRule(
        title=req.title,
        description=req.description,
        severity=req.severity,
        category=req.category,
        mitre_attack_id=req.mitre_attack_id,
        condition=cond,
        active=req.active
    )
    if req.rule_id:
        new_rule.rule_id = req.rule_id
    registered = detection_service.registry.add_rule(new_rule)
    return RuleDTO(
        rule_id=registered.rule_id,
        title=registered.title,
        description=registered.description,
        severity=registered.severity,
        category=registered.category,
        mitre_attack_id=registered.mitre_attack_id,
        active=registered.active
    )

@router.put("/rules/{rule_id}", response_model=RuleDTO)
async def update_rule(rule_id: str, req: UpdateRuleRequest):
    """Updates an existing detection rule."""
    updated = detection_service.registry.update_rule(rule_id, req.title, req.description, req.severity, req.active)
    if not updated:
        raise HTTPException(status_code=404, detail="Rule not found")
    return RuleDTO(
        rule_id=updated.rule_id,
        title=updated.title,
        description=updated.description,
        severity=updated.severity,
        category=updated.category,
        mitre_attack_id=updated.mitre_attack_id,
        active=updated.active
    )

@router.post("/rules/{rule_id}/enable", response_model=RuleDTO)
async def enable_rule(rule_id: str):
    """Enables a detection rule."""
    rule = detection_service.registry.enable_rule(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return RuleDTO(rule_id=rule.rule_id, title=rule.title, description=rule.description, severity=rule.severity, category=rule.category, mitre_attack_id=rule.mitre_attack_id, active=rule.active)

@router.post("/rules/{rule_id}/disable", response_model=RuleDTO)
async def disable_rule(rule_id: str):
    """Disables a detection rule."""
    rule = detection_service.registry.disable_rule(rule_id)
    if not rule:
        raise HTTPException(status_code=404, detail="Rule not found")
    return RuleDTO(rule_id=rule.rule_id, title=rule.title, description=rule.description, severity=rule.severity, category=rule.category, mitre_attack_id=rule.mitre_attack_id, active=rule.active)

@router.post("/rules/test")
async def test_rule(req: TestRuleRequest):
    """Tests a rule condition against a sample event payload."""
    event_dict = req.sample_event
    cond = req.rule.condition
    field_path = cond.field_path.split(".")
    val = event_dict
    for p in field_path:
        if isinstance(val, dict) and p in val:
            val = val[p]
        else:
            val = None
            break
    matched = (str(val) == str(cond.target_value)) if val is not None else False
    return {"rule_title": req.rule.title, "matched": matched, "evaluated_value": val, "expected_value": cond.target_value}

@router.post("/evaluate", response_model=List[FindingDTO])
async def evaluate_event(req: EvaluateEventRequest):
    """Evaluates a normalized event payload against active detection rules."""
    norm_event = NormalizedEvent(
        organization_id=req.organization_id,
        source=EventSource(ip=req.source_ip),
        destination=EventDestination(asset_id=req.asset_id),
        event=EventClassification(category=req.event_type, action=req.action, severity="HIGH")
    )
    findings = await detection_service.process_normalized_event(norm_event)
    return [
        FindingDTO(
            finding_id=f.finding_id,
            organization_id=f.organization_id,
            rule_id=f.rule_id,
            rule_title=f.rule_title,
            severity=f.severity,
            asset_id=f.asset_id,
            source_ip=f.source_ip,
            matched_event_ids=f.matched_event_ids,
            confidence_score=f.confidence_score
        ) for f in findings
    ]

# 2. FINDINGS ENDPOINTS
@router.get("/findings", response_model=List[FindingDTO])
async def list_findings(x_organization_id: Optional[str] = Header(None)):
    """Returns detected findings for tenant (BR-0004)."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    findings = detection_service.list_findings(org_id)
    return [
        FindingDTO(
            finding_id=f.finding_id,
            organization_id=f.organization_id,
            rule_id=f.rule_id,
            rule_title=f.rule_title,
            severity=f.severity,
            asset_id=f.asset_id,
            source_ip=f.source_ip,
            matched_event_ids=f.matched_event_ids,
            confidence_score=f.confidence_score
        ) for f in findings
    ]

@router.get("/findings/{finding_id}", response_model=FindingDTO)
async def get_finding(finding_id: str):
    """Retrieves a single finding by ID."""
    finding = detection_service.get_finding(finding_id)
    if not finding:
        raise HTTPException(status_code=404, detail="Finding not found")
    return FindingDTO(
        finding_id=finding.finding_id,
        organization_id=finding.organization_id,
        rule_id=finding.rule_id,
        rule_title=finding.rule_title,
        severity=finding.severity,
        asset_id=finding.asset_id,
        source_ip=finding.source_ip,
        matched_event_ids=finding.matched_event_ids,
        confidence_score=finding.confidence_score
    )

# 3. ALERTS ENDPOINTS
@router.get("/alerts", response_model=List[ActionableAlertDTO])
async def list_detection_alerts(x_organization_id: Optional[str] = Header(None)):
    """Returns promoted actionable alerts for tenant (BR-0004)."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    alerts = detection_service.list_alerts(org_id)
    return [
        ActionableAlertDTO(
            alert_id=a.alert_id,
            organization_id=a.organization_id,
            rule_id=a.rule_id,
            title=a.title,
            severity=a.severity,
            asset_id=a.asset_id,
            source_ip=a.source_ip,
            status=a.status,
            mitre_attack_id=a.mitre_attack_id,
            findings_count=a.findings_count,
            first_seen=a.first_seen.isoformat(),
            last_seen=a.last_seen.isoformat()
        ) for a in alerts
    ]

@router.get("/alerts/{alert_id}", response_model=ActionableAlertDTO)
async def get_alert(alert_id: str):
    """Retrieves a single alert by ID."""
    alert = detection_service.get_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return ActionableAlertDTO(
        alert_id=alert.alert_id,
        organization_id=alert.organization_id,
        rule_id=alert.rule_id,
        title=alert.title,
        severity=alert.severity,
        asset_id=alert.asset_id,
        source_ip=alert.source_ip,
        status=alert.status,
        mitre_attack_id=alert.mitre_attack_id,
        findings_count=alert.findings_count,
        first_seen=alert.first_seen.isoformat(),
        last_seen=alert.last_seen.isoformat()
    )

@router.patch("/alerts/{alert_id}/status", response_model=ActionableAlertDTO)
async def update_alert_status(alert_id: str, req: UpdateAlertStatusRequest):
    """Updates alert status."""
    updated = detection_service.update_alert_status(alert_id, req.status)
    if not updated:
        raise HTTPException(status_code=404, detail="Alert not found or invalid status transition.")
    return ActionableAlertDTO(
        alert_id=updated.alert_id,
        organization_id=updated.organization_id,
        rule_id=updated.rule_id,
        title=updated.title,
        severity=updated.severity,
        asset_id=updated.asset_id,
        source_ip=updated.source_ip,
        status=updated.status,
        mitre_attack_id=updated.mitre_attack_id,
        findings_count=updated.findings_count,
        first_seen=updated.first_seen.isoformat(),
        last_seen=updated.last_seen.isoformat()
    )

@router.post("/alerts/{alert_id}/acknowledge", response_model=ActionableAlertDTO)
async def acknowledge_alert(alert_id: str):
    """Acknowledges an alert (NEW -> ACKNOWLEDGED)."""
    updated = detection_service.update_alert_status(alert_id, "ACKNOWLEDGED")
    if not updated:
        raise HTTPException(status_code=404, detail="Alert not found")
    return ActionableAlertDTO(alert_id=updated.alert_id, organization_id=updated.organization_id, rule_id=updated.rule_id, title=updated.title, severity=updated.severity, asset_id=updated.asset_id, source_ip=updated.source_ip, status=updated.status, mitre_attack_id=updated.mitre_attack_id, findings_count=updated.findings_count, first_seen=updated.first_seen.isoformat(), last_seen=updated.last_seen.isoformat())

@router.post("/alerts/{alert_id}/assign", response_model=ActionableAlertDTO)
async def assign_alert(alert_id: str, req: AssignAlertRequest):
    """Assigns an alert to a SOC analyst."""
    updated = detection_service.update_alert_status(alert_id, "IN_PROGRESS")
    if not updated:
        raise HTTPException(status_code=404, detail="Alert not found")
    return ActionableAlertDTO(alert_id=updated.alert_id, organization_id=updated.organization_id, rule_id=updated.rule_id, title=updated.title, severity=updated.severity, asset_id=updated.asset_id, source_ip=updated.source_ip, status=updated.status, mitre_attack_id=updated.mitre_attack_id, findings_count=updated.findings_count, first_seen=updated.first_seen.isoformat(), last_seen=updated.last_seen.isoformat())

@router.post("/alerts/{alert_id}/suppress", response_model=ActionableAlertDTO)
async def suppress_alert(alert_id: str):
    """Suppresses an alert."""
    updated = detection_service.update_alert_status(alert_id, "SUPPRESSED")
    if not updated:
        raise HTTPException(status_code=404, detail="Alert not found")
    return ActionableAlertDTO(alert_id=updated.alert_id, organization_id=updated.organization_id, rule_id=updated.rule_id, title=updated.title, severity=updated.severity, asset_id=updated.asset_id, source_ip=updated.source_ip, status=updated.status, mitre_attack_id=updated.mitre_attack_id, findings_count=updated.findings_count, first_seen=updated.first_seen.isoformat(), last_seen=updated.last_seen.isoformat())

@router.post("/alerts/{alert_id}/close", response_model=ActionableAlertDTO)
async def close_alert(alert_id: str):
    """Closes an alert."""
    updated = detection_service.update_alert_status(alert_id, "CLOSED")
    if not updated:
        raise HTTPException(status_code=404, detail="Alert not found")
    return ActionableAlertDTO(alert_id=updated.alert_id, organization_id=updated.organization_id, rule_id=updated.rule_id, title=updated.title, severity=updated.severity, asset_id=updated.asset_id, source_ip=updated.source_ip, status=updated.status, mitre_attack_id=updated.mitre_attack_id, findings_count=updated.findings_count, first_seen=updated.first_seen.isoformat(), last_seen=updated.last_seen.isoformat())

@router.post("/alerts/{alert_id}/reopen", response_model=ActionableAlertDTO)
async def reopen_alert(alert_id: str):
    """Reopens a closed or suppressed alert."""
    updated = detection_service.update_alert_status(alert_id, "NEW")
    if not updated:
        raise HTTPException(status_code=404, detail="Alert not found")
    return ActionableAlertDTO(alert_id=updated.alert_id, organization_id=updated.organization_id, rule_id=updated.rule_id, title=updated.title, severity=updated.severity, asset_id=updated.asset_id, source_ip=updated.source_ip, status=updated.status, mitre_attack_id=updated.mitre_attack_id, findings_count=updated.findings_count, first_seen=updated.first_seen.isoformat(), last_seen=updated.last_seen.isoformat())
