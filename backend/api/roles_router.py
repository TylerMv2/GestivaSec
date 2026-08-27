"""
Gestiva Security (GestivaSec V1) — IAM-ROLES: Roles REST API Router
Exposes /api/v1/roles endpoints.
"""
from typing import List, Set
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.application.role_service import RoleApplicationService

router = APIRouter(prefix="/api/v1/roles", tags=["Role Management"])
role_service = RoleApplicationService()

class RoleResponse(BaseModel):
    name: str
    description: str
    permissions: Set[str]

@router.get("", response_model=List[RoleResponse])
async def list_roles():
    """Lists all configured RBAC roles and permissions."""
    roles = await role_service.list_roles()
    return [
        RoleResponse(
            name=r.name,
            description=r.description,
            permissions=r.permissions
        )
        for r in roles
    ]

@router.get("/{role_name}", response_model=RoleResponse)
async def get_role(role_name: str):
    """Retrieves specific RBAC role details."""
    role = await role_service.get_role(role_name)
    if not role:
        raise HTTPException(status_code=404, detail=f"Rol '{role_name}' no encontrado.")
    return RoleResponse(
        name=role.name,
        description=role.description,
        permissions=role.permissions
    )
