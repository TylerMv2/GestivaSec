"""
Gestiva Security (GestivaSec V1) — IAM-PERMS: Permissions REST API Router
Exposes /api/v1/permissions endpoints.
"""
from typing import Set
from fastapi import APIRouter, Query
from pydantic import BaseModel

from backend.domain.permission import PermissionEvaluator

router = APIRouter(prefix="/api/v1/permissions", tags=["Permissions Engine"])

class PermissionCheckResponse(BaseModel):
    role: str
    permission: str
    is_authorized: bool

class RolePermissionsResponse(BaseModel):
    role: str
    permissions: Set[str]

@router.get("/check", response_model=PermissionCheckResponse)
async def check_permission(
    role: str = Query(..., example="SOC_ANALYST"),
    permission: str = Query(..., example="assets:read")
):
    """Evaluates whether role possesses required permission."""
    authorized = PermissionEvaluator.is_authorized(role, permission)
    return PermissionCheckResponse(
        role=role,
        permission=permission,
        is_authorized=authorized
    )

@router.get("/{role_name}", response_model=RolePermissionsResponse)
async def get_permissions(role_name: str):
    """Retrieves all granted permissions for a given role."""
    perms = PermissionEvaluator.get_role_permissions(role_name)
    return RolePermissionsResponse(
        role=role_name,
        permissions=perms
    )
