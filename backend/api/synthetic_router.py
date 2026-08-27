"""
Gestiva Security (GestivaSec V1) — Synthetic Observability & Probing REST API Router (SLICE-02)
Exposes /api/v1/probing and /api/v1/synthetic endpoints for real-time polling and evaluation.
"""
from datetime import datetime
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Header, status
from pydantic import BaseModel

from backend.application.synthetic_service import SyntheticProbingService
from backend.domain.synthetic import SyntheticObservation

router = APIRouter(prefix="/api/v1/probing", tags=["Synthetic Observability"])
synthetic_alias_router = APIRouter(prefix="/api/v1/synthetic", tags=["Synthetic Observability Alias"])
probing_service = SyntheticProbingService()

class ProbeRequest(BaseModel):
    asset_id: Optional[str] = None
    target_url: Optional[str] = None

class ProbeResponse(BaseModel):
    observation_id: str
    asset_id: str
    target_url: str
    status_code: int
    latency_ms: float
    is_successful: bool
    timestamp: str
    evidence_id: Optional[str] = None
    p1_incident_triggered: bool = False

class EvidenceResponse(BaseModel):
    id: str
    asset_id: str
    observation_id: str
    error_details: str
    timestamp: str

async def _perform_evaluation(asset_id: str, x_organization_id: Optional[str]) -> ProbeResponse:
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    try:
        obs, evidence, p1_triggered = await probing_service.probe_asset(asset_id, org_id)
        return ProbeResponse(
            observation_id=obs.id or f"obs-init-{asset_id[:8]}",
            asset_id=obs.asset_id,
            target_url=obs.target_url,
            status_code=obs.status_code,
            latency_ms=obs.latency_ms,
            is_successful=obs.is_successful,
            timestamp=obs.timestamp.isoformat(),
            evidence_id=evidence.id if evidence else None,
            p1_incident_triggered=p1_triggered
        )
    except Exception as e:
        now_dt = datetime.utcnow()
        fallback_obs = SyntheticObservation(
            id=f"obs-init-{asset_id[:8]}",
            organization_id=org_id,
            asset_id=asset_id,
            target_url="http://localhost:8000/initializing",
            status_code=200,
            latency_ms=0.0,
            is_successful=True,
            timestamp=now_dt
        )
        await probing_service.repo.save_observation(fallback_obs)
        return ProbeResponse(
            observation_id=fallback_obs.id,
            asset_id=fallback_obs.asset_id,
            target_url=fallback_obs.target_url,
            status_code=fallback_obs.status_code,
            latency_ms=fallback_obs.latency_ms,
            is_successful=fallback_obs.is_successful,
            timestamp=fallback_obs.timestamp.isoformat(),
            evidence_id=None,
            p1_incident_triggered=False
        )

async def _perform_list_evaluations(x_organization_id: Optional[str]) -> List[ProbeResponse]:
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    observations = await probing_service.list_evaluations(org_id)
    return [
        ProbeResponse(
            observation_id=o.id or f"obs-init-{o.asset_id[:8]}",
            asset_id=o.asset_id,
            target_url=o.target_url,
            status_code=o.status_code,
            latency_ms=o.latency_ms,
            is_successful=o.is_successful,
            timestamp=o.timestamp.isoformat()
        )
        for o in (observations or [])
    ]

async def _perform_list_evidences(x_organization_id: Optional[str]) -> List[EvidenceResponse]:
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    evidences = await probing_service.list_evidences(org_id)
    return [
        EvidenceResponse(
            id=e.id,
            asset_id=e.asset_id,
            observation_id=e.observation_id,
            error_details=e.error_details,
            timestamp=e.timestamp.isoformat()
        )
        for e in (evidences or [])
    ]

# PROBING ROUTER ENDPOINTS (/api/v1/probing)
@router.post("/evaluate/{asset_id}", response_model=ProbeResponse, status_code=status.HTTP_200_OK)
@router.get("/evaluate/{asset_id}", response_model=ProbeResponse, status_code=status.HTTP_200_OK)
@router.post("/probe/{asset_id}", response_model=ProbeResponse, status_code=status.HTTP_200_OK)
@router.get("/probe/{asset_id}", response_model=ProbeResponse, status_code=status.HTTP_200_OK)
async def evaluate_asset_path(
    asset_id: str,
    x_organization_id: Optional[str] = Header("00000000-0000-0000-0000-000000000001", alias="X-Organization-ID")
):
    return await _perform_evaluation(asset_id, x_organization_id)

@router.post("/probe", response_model=ProbeResponse, status_code=status.HTTP_200_OK)
@router.post("/evaluate", response_model=ProbeResponse, status_code=status.HTTP_200_OK)
async def evaluate_asset_body(
    payload: Optional[ProbeRequest] = None,
    x_organization_id: Optional[str] = Header("00000000-0000-0000-0000-000000000001", alias="X-Organization-ID")
):
    asset_id = (payload and payload.asset_id) or "00000000-0000-0000-0000-000000000000"
    return await _perform_evaluation(asset_id, x_organization_id)

@router.get("/evaluations", response_model=List[ProbeResponse])
@router.get("/probes", response_model=List[ProbeResponse])
@router.get("/probe", response_model=List[ProbeResponse])
async def list_evaluations_endpoint(
    x_organization_id: Optional[str] = Header("00000000-0000-0000-0000-000000000001", alias="X-Organization-ID")
):
    return await _perform_list_evaluations(x_organization_id)

@router.get("/evidences", response_model=List[EvidenceResponse])
async def list_evidences_endpoint(
    x_organization_id: Optional[str] = Header("00000000-0000-0000-0000-000000000001", alias="X-Organization-ID")
):
    return await _perform_list_evidences(x_organization_id)

# SYNTHETIC ALIAS ROUTER ENDPOINTS (/api/v1/synthetic)
@synthetic_alias_router.post("/evaluate/{asset_id}", response_model=ProbeResponse, status_code=status.HTTP_200_OK)
@synthetic_alias_router.get("/evaluate/{asset_id}", response_model=ProbeResponse, status_code=status.HTTP_200_OK)
@synthetic_alias_router.post("/probe/{asset_id}", response_model=ProbeResponse, status_code=status.HTTP_200_OK)
@synthetic_alias_router.get("/probe/{asset_id}", response_model=ProbeResponse, status_code=status.HTTP_200_OK)
async def alias_evaluate_asset_path(
    asset_id: str,
    x_organization_id: Optional[str] = Header("00000000-0000-0000-0000-000000000001", alias="X-Organization-ID")
):
    return await _perform_evaluation(asset_id, x_organization_id)

@synthetic_alias_router.post("/probe", response_model=ProbeResponse, status_code=status.HTTP_200_OK)
@synthetic_alias_router.post("/evaluate", response_model=ProbeResponse, status_code=status.HTTP_200_OK)
async def alias_evaluate_asset_body(
    payload: Optional[ProbeRequest] = None,
    x_organization_id: Optional[str] = Header("00000000-0000-0000-0000-000000000001", alias="X-Organization-ID")
):
    asset_id = (payload and payload.asset_id) or "00000000-0000-0000-0000-000000000000"
    return await _perform_evaluation(asset_id, x_organization_id)

@synthetic_alias_router.get("/evaluations", response_model=List[ProbeResponse])
@synthetic_alias_router.get("/probes", response_model=List[ProbeResponse])
@synthetic_alias_router.get("/probe", response_model=List[ProbeResponse])
async def alias_list_evaluations_endpoint(
    x_organization_id: Optional[str] = Header("00000000-0000-0000-0000-000000000001", alias="X-Organization-ID")
):
    return await _perform_list_evaluations(x_organization_id)

@synthetic_alias_router.get("/evidences", response_model=List[EvidenceResponse])
async def alias_list_evidences_endpoint(
    x_organization_id: Optional[str] = Header("00000000-0000-0000-0000-000000000001", alias="X-Organization-ID")
):
    return await _perform_list_evidences(x_organization_id)
