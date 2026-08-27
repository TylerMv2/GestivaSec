"""
Gestiva Security (GestivaSec V1) — IAM-ROLES: Role Repository Persistence Adapter
"""
from typing import List, Optional
from backend.domain.role import RoleDefinition, RoleMatrix

class RoleRepository:
    async def get_by_name(self, name: str) -> Optional[RoleDefinition]:
        try:
            return RoleMatrix.get_role(name)
        except ValueError:
            return None

    async def list_all(self) -> List[RoleDefinition]:
        return RoleMatrix.list_roles()
