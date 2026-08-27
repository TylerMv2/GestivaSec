"""
Gestiva Security (GestivaSec V1) — IAM-ROLES: Role Application Service
"""
from typing import List, Optional
from backend.domain.role import RoleDefinition
from backend.infrastructure.role_repository import RoleRepository

class RoleApplicationService:
    def __init__(self, repo: Optional[RoleRepository] = None):
        self.repo = repo or RoleRepository()

    async def list_roles(self) -> List[RoleDefinition]:
        return await self.repo.list_all()

    async def get_role(self, role_name: str) -> Optional[RoleDefinition]:
        return await self.repo.get_by_name(role_name)
