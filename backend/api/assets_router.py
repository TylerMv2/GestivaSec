"""
Gestiva Security (GestivaSec V1) — SPRINT 3: Asset Intelligence REST API Router
Exposes CMDB-grade Asset Management: Lifecycle transitions, IP forensic history, Risk Scoring & Asset Intelligence.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, status, Header
from pydantic import BaseModel, EmailStr, Field

from backend.domain.asset import DigitalAsset
from backend.infrastructure.asset_repository import AssetRepository
from backend.application.auth_service import AuthenticationService
from shared.constants import AssetStatus

router = APIRouter(prefix="/api/v1/assets", tags=["Asset Intelligence Engine"])
asset_repo = AssetRepository()
auth_service = AuthenticationService()

class CreateAssetRequest(BaseModel):
    name: str = Field(..., json_schema_extra={"example": "GestivaOne Portal"})
    target_url: str = Field(..., json_schema_extra={"example": "https://gestivaone.com"})
    criticality: str = Field("P3_MEDIUM", json_schema_extra={"example": "P1_CRITICAL"})
    owner_email: EmailStr = Field(..., json_schema_extra={"example": "ops@gestivaone.com"})
    department: Optional[str] = "IT Operations"
    os_family: Optional[str] = "Linux / Ubuntu 22.04"

class UpdateLifecycleRequest(BaseModel):
    status: AssetStatus

class UpdateLocationRequest(BaseModel):
    new_target_url: str

class IPHistoryDTO(BaseModel):
    ip_address: str
    assigned_at: str

class AssetResponse(BaseModel):
    id: str
    organization_id: str
    name: str
    target_url: str
    criticality: str
    owner_email: str
    status: str
    department: str
    business_unit: str
    os_family: str
    fingerprint_confidence: float
    risk_score: float
    tags: List[str]
    ip_history: List[IPHistoryDTO]
    last_seen: str
    created_at: str

@router.get("", response_model=List[AssetResponse])
async def list_assets(
    x_organization_id: Optional[str] = Header(None)
):
    """Returns digital assets with full Asset Intelligence for the organization (BR-0004)."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    assets = await asset_repo.list_by_organization(org_id)
    return [
        AssetResponse(
            id=a.id,
            organization_id=a.organization_id,
            name=a.name,
            target_url=a.target_url,
            criticality=a.criticality,
            owner_email=a.owner_email,
            status=a.status if isinstance(a.status, str) else a.status.value,
            department=a.department,
            business_unit=a.business_unit,
            os_family=a.os_family,
            fingerprint_confidence=a.fingerprint_confidence,
            risk_score=a.calculate_risk_score(),
            tags=a.tags,
            ip_history=[
                IPHistoryDTO(ip_address=h.ip_address, assigned_at=h.assigned_at.isoformat())
                for h in a.ip_history
            ],
            last_seen=a.last_seen.isoformat() if a.last_seen else "",
            created_at=a.created_at.isoformat() if a.created_at else ""
        ) for a in assets
    ]

@router.post("", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(
    payload: CreateAssetRequest,
    x_organization_id: Optional[str] = Header(None)
):
    """Registers a new Digital Asset into the CMDB Inventory."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    try:
        asset = DigitalAsset(
            id=None,
            organization_id=org_id,
            name=payload.name,
            target_url=payload.target_url,
            criticality=payload.criticality,
            owner_email=payload.owner_email,
            department=payload.department or "IT Operations",
            os_family=payload.os_family or "Linux / Unix",
            status=AssetStatus.ACTIVE
        )
        saved = await asset_repo.create(asset)
        return AssetResponse(
            id=saved.id,
            organization_id=saved.organization_id,
            name=saved.name,
            target_url=saved.target_url,
            criticality=saved.criticality,
            owner_email=saved.owner_email,
            status=saved.status if isinstance(saved.status, str) else saved.status.value,
            department=saved.department,
            business_unit=saved.business_unit,
            os_family=saved.os_family,
            fingerprint_confidence=saved.fingerprint_confidence,
            risk_score=saved.calculate_risk_score(),
            tags=saved.tags,
            ip_history=[],
            last_seen=saved.last_seen.isoformat() if saved.last_seen else "",
            created_at=saved.created_at.isoformat() if saved.created_at else ""
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.patch("/{asset_id}/lifecycle", response_model=AssetResponse)
async def transition_asset_lifecycle(
    asset_id: str,
    payload: UpdateLifecycleRequest,
    x_organization_id: Optional[str] = Header(None)
):
    """Executes a Lifecycle State Machine transition for an Asset."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    asset = await asset_repo.get_by_id(asset_id, org_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset no encontrado.")

    asset.transition_lifecycle(payload.status)
    return AssetResponse(
        id=asset.id,
        organization_id=asset.organization_id,
        name=asset.name,
        target_url=asset.target_url,
        criticality=asset.criticality,
        owner_email=asset.owner_email,
        status=asset.status if isinstance(asset.status, str) else asset.status.value,
        department=asset.department,
        business_unit=asset.business_unit,
        os_family=asset.os_family,
        fingerprint_confidence=asset.fingerprint_confidence,
        risk_score=asset.calculate_risk_score(),
        tags=asset.tags,
        ip_history=[
            IPHistoryDTO(ip_address=h.ip_address, assigned_at=h.assigned_at.isoformat())
            for h in asset.ip_history
        ],
        last_seen=asset.last_seen.isoformat() if asset.last_seen else "",
        created_at=asset.created_at.isoformat() if asset.created_at else ""
    )

@router.post("/{asset_id}/location", response_model=AssetResponse)
async def update_asset_location(
    asset_id: str,
    payload: UpdateLocationRequest,
    x_organization_id: Optional[str] = Header(None)
):
    """Updates Asset URL/IP location and logs historical record to ip_history."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    asset = await asset_repo.get_by_id(asset_id, org_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset no encontrado.")

    asset.update_location(payload.new_target_url)
    return AssetResponse(
        id=asset.id,
        organization_id=asset.organization_id,
        name=asset.name,
        target_url=asset.target_url,
        criticality=asset.criticality,
        owner_email=asset.owner_email,
        status=asset.status if isinstance(asset.status, str) else asset.status.value,
        department=asset.department,
        business_unit=asset.business_unit,
        os_family=asset.os_family,
        fingerprint_confidence=asset.fingerprint_confidence,
        risk_score=asset.calculate_risk_score(),
        tags=asset.tags,
        ip_history=[
            IPHistoryDTO(ip_address=h.ip_address, assigned_at=h.assigned_at.isoformat())
            for h in asset.ip_history
        ],
        last_seen=asset.last_seen.isoformat() if asset.last_seen else "",
        created_at=asset.created_at.isoformat() if asset.created_at else ""
    )
