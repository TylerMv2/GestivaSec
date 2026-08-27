"""
Gestiva Security (GestivaSec V1) — IAM-USERS: User Management REST API Router
Exposes /api/v1/users endpoints.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Header, status
from pydantic import BaseModel, EmailStr, Field

from backend.application.user_service import UserApplicationService

router = APIRouter(prefix="/api/v1/users", tags=["User Management"])
user_service = UserApplicationService()

class UserCreateRequest(BaseModel):
    email: EmailStr = Field(..., example="analyst@gestivaone.com")
    password: str = Field(..., example="AnalystSec2026!")
    role: str = Field("SOC_ANALYST", example="SOC_ANALYST")

class UserResponse(BaseModel):
    id: str
    organization_id: str
    email: str
    role: str
    is_active: bool
    created_at: str

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    payload: UserCreateRequest,
    x_organization_id: Optional[str] = Header("00000000-0000-0000-0000-000000000001", alias="X-Organization-ID")
):
    """Registers a new SOC analyst user in the organization boundary."""
    try:
        user = await user_service.register_user(
            organization_id=x_organization_id,
            email=payload.email,
            plain_password=payload.password,
            role=payload.role
        )
        return UserResponse(
            id=user.id,
            organization_id=user.organization_id,
            email=user.email,
            role=user.role,
            is_active=user.is_active,
            created_at=user.created_at.isoformat() if user.created_at else ""
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[UserResponse])
async def list_users(
    x_organization_id: Optional[str] = Header("00000000-0000-0000-0000-000000000001", alias="X-Organization-ID")
):
    """Lists all users belonging to the organization."""
    users = await user_service.list_users(organization_id=x_organization_id)
    return [
        UserResponse(
            id=u.id,
            organization_id=u.organization_id,
            email=u.email,
            role=u.role,
            is_active=u.is_active,
            created_at=u.created_at.isoformat() if u.created_at else ""
        )
        for u in users
    ]
