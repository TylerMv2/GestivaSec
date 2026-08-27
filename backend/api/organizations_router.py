"""
Gestiva Security (GestivaSec V1) — Organizations REST API Router (SLICE-002)
Exposes /api/v1/organizations endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Header, status
from pydantic import BaseModel, Field

from backend.application.organization_service import OrganizationApplicationService

router = APIRouter(prefix="/api/v1/organizations", tags=["Organizations"])
org_service = OrganizationApplicationService()

class OrganizationCreateRequest(BaseModel):
    name: str = Field(..., example="GestivaOne Enterprise")

class OrganizationResponse(BaseModel):
    id: str
    name: str
    slug: str
    status: str
    created_at: str

@router.post("", response_model=OrganizationResponse, status_code=status.HTTP_201_CREATED)
async def create_organization(payload: OrganizationCreateRequest):
    """Registers a new organization tenant boundary."""
    try:
        org = await org_service.create_organization(payload.name)
        return OrganizationResponse(
            id=org.id,
            name=org.name,
            slug=org.slug,
            status=org.status,
            created_at=org.created_at.isoformat() if org.created_at else ""
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[OrganizationResponse])
async def list_organizations():
    """Lists all registered organizations."""
    orgs = await org_service.list_organizations()
    return [
        OrganizationResponse(
            id=o.id,
            name=o.name,
            slug=o.slug,
            status=o.status,
            created_at=o.created_at.isoformat() if o.created_at else ""
        )
        for o in orgs
    ]

@router.get("/current", response_model=OrganizationResponse)
async def get_current_organization(
    x_organization_id: Optional[str] = Header("00000000-0000-0000-0000-000000000001", alias="X-Organization-ID")
):
    """Retrieves active organization details based on tenant header."""
    org = await org_service.get_organization(x_organization_id)
    if not org:
        raise HTTPException(status_code=404, detail="Organización activa no encontrada.")
    return OrganizationResponse(
        id=org.id,
        name=org.name,
        slug=org.slug,
        status=org.status,
        created_at=org.created_at.isoformat() if org.created_at else ""
    )
