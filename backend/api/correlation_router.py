"""
Gestiva Security (GestivaSec V1) — SPRINT 7: Multi-Event Correlation REST API Router
Exposes GET /api/v1/correlation/chains, /chains/{chain_id}, /chains/{chain_id}/timeline, and /rules.
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Header
from pydantic import BaseModel, Field

from backend.application.correlation_service import CorrelationEngineService
from backend.domain.correlation import CorrelationRule

router = APIRouter(prefix="/api/v1/correlation", tags=["Multi-Event Correlation Engine"])
correlation_service = CorrelationEngineService()

class NodeDTO(BaseModel):
    finding_id: str
    rule_id: str
    rule_title: str
    severity: str
    mitre_phase: str
    timestamp: str

class AttackChainDTO(BaseModel):
    chain_id: str
    organization_id: str
    asset_id: Optional[str]
    target_ip: str
    chain_title: str
    severity: str
    status: str
    correlation_score: int
    confidence_score: float
    explainable_reasons: List[str]
    nodes: List[NodeDTO]
    kill_chain_stages: List[str]
    first_seen: str
    last_seen: str

class CorrelationRuleDTO(BaseModel):
    rule_id: str
    organization_id: str
    name: str
    description: str
    enabled: bool
    version: str
    time_window_minutes: int
    required_event_count: int
    severity: str
    mitre_attack_techniques: List[str]

class CreateCorrelationRuleRequest(BaseModel):
    name: str
    description: str
    time_window_minutes: int = 15
    required_event_count: int = 2
    severity: str = "P1_CRITICAL"
    mitre_attack_techniques: List[str] = Field(default_factory=lambda: ["T1110.001", "T1068"])

@router.get("/chains", response_model=List[AttackChainDTO])
async def list_attack_chains(x_organization_id: Optional[str] = Header(None)):
    """Returns correlated attack chain graphs for tenant (BR-0004)."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    chains = correlation_service.list_attack_chains(org_id)
    return [
        AttackChainDTO(
            chain_id=c.chain_id,
            organization_id=c.organization_id,
            asset_id=c.asset_id,
            target_ip=c.target_ip,
            chain_title=c.chain_title,
            severity=c.severity,
            status=c.status,
            correlation_score=c.correlation_score,
            confidence_score=c.confidence_score,
            explainable_reasons=c.explainable_reasons,
            nodes=[
                NodeDTO(
                    finding_id=n.finding_id,
                    rule_id=n.rule_id,
                    rule_title=n.rule_title,
                    severity=n.severity,
                    mitre_phase=n.mitre_phase,
                    timestamp=n.timestamp.isoformat()
                ) for n in c.nodes
            ],
            kill_chain_stages=c.kill_chain_stages,
            first_seen=c.first_seen.isoformat(),
            last_seen=c.last_seen.isoformat()
        ) for c in chains
    ]

@router.get("/chains/{chain_id}", response_model=AttackChainDTO)
async def get_attack_chain(chain_id: str):
    """Retrieves a single attack chain graph by ID."""
    chain = correlation_service.get_attack_chain(chain_id)
    if not chain:
        raise HTTPException(status_code=404, detail="Attack chain not found")
    return AttackChainDTO(
        chain_id=chain.chain_id,
        organization_id=chain.organization_id,
        asset_id=chain.asset_id,
        target_ip=chain.target_ip,
        chain_title=chain.chain_title,
        severity=chain.severity,
        status=chain.status,
        correlation_score=chain.correlation_score,
        confidence_score=chain.confidence_score,
        explainable_reasons=chain.explainable_reasons,
        nodes=[
            NodeDTO(
                finding_id=n.finding_id,
                rule_id=n.rule_id,
                rule_title=n.rule_title,
                severity=n.severity,
                mitre_phase=n.mitre_phase,
                timestamp=n.timestamp.isoformat()
            ) for n in chain.nodes
        ],
        kill_chain_stages=chain.kill_chain_stages,
        first_seen=chain.first_seen.isoformat(),
        last_seen=chain.last_seen.isoformat()
    )

@router.get("/chains/{chain_id}/timeline")
async def get_attack_chain_timeline(chain_id: str):
    """Retrieves chronological chain timeline events."""
    timeline = correlation_service.get_chain_timeline(chain_id)
    if timeline is None:
        raise HTTPException(status_code=404, detail="Attack chain timeline not found")
    return {"chain_id": chain_id, "timeline": timeline}

@router.get("/rules", response_model=List[CorrelationRuleDTO])
async def list_correlation_rules(x_organization_id: Optional[str] = Header(None)):
    """Lists correlation rules for tenant."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    rules = correlation_service.list_rules(org_id)
    return [
        CorrelationRuleDTO(
            rule_id=r.rule_id,
            organization_id=r.organization_id,
            name=r.name,
            description=r.description,
            enabled=r.enabled,
            version=r.version,
            time_window_minutes=r.time_window_minutes,
            required_event_count=r.required_event_count,
            severity=r.severity,
            mitre_attack_techniques=r.mitre_attack_techniques
        ) for r in rules
    ]

@router.post("/rules", response_model=CorrelationRuleDTO, status_code=201)
async def create_correlation_rule(req: CreateCorrelationRuleRequest, x_organization_id: Optional[str] = Header(None)):
    """Creates a new tenant correlation rule."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    rule = CorrelationRule(
        organization_id=org_id,
        name=req.name,
        description=req.description,
        time_window_minutes=req.time_window_minutes,
        required_event_count=req.required_event_count,
        severity=req.severity,
        mitre_attack_techniques=req.mitre_attack_techniques
    )
    created = correlation_service.add_rule(rule)
    return CorrelationRuleDTO(
        rule_id=created.rule_id,
        organization_id=created.organization_id,
        name=created.name,
        description=created.description,
        enabled=created.enabled,
        version=created.version,
        time_window_minutes=created.time_window_minutes,
        required_event_count=created.required_event_count,
        severity=created.severity,
        mitre_attack_techniques=created.mitre_attack_techniques
    )

@router.post("/chains/{chain_id}/close", response_model=AttackChainDTO)
async def close_attack_chain(chain_id: str):
    """Resolves/Closes an attack chain."""
    closed = correlation_service.close_attack_chain(chain_id)
    if not closed:
        raise HTTPException(status_code=404, detail="Attack chain not found")
    return AttackChainDTO(
        chain_id=closed.chain_id,
        organization_id=closed.organization_id,
        asset_id=closed.asset_id,
        target_ip=closed.target_ip,
        chain_title=closed.chain_title,
        severity=closed.severity,
        status=closed.status,
        correlation_score=closed.correlation_score,
        confidence_score=closed.confidence_score,
        explainable_reasons=closed.explainable_reasons,
        nodes=[
            NodeDTO(
                finding_id=n.finding_id,
                rule_id=n.rule_id,
                rule_title=n.rule_title,
                severity=n.severity,
                mitre_phase=n.mitre_phase,
                timestamp=n.timestamp.isoformat()
            ) for n in closed.nodes
        ],
        kill_chain_stages=closed.kill_chain_stages,
        first_seen=closed.first_seen.isoformat(),
        last_seen=closed.last_seen.isoformat()
    )
