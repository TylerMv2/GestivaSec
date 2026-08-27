"""
Gestiva Security (GestivaSec V1) — IAM-PERMS: Granular Permissions Engine
Enforces Role-to-Permission evaluation and action authorization.
"""
from dataclasses import dataclass
from typing import Set
from backend.domain.role import RoleMatrix

@dataclass
class PermissionEvaluator:
    @staticmethod
    def is_authorized(role_name: str, required_permission: str) -> bool:
        """Evaluates whether role possesses required permission."""
        try:
            role = RoleMatrix.get_role(role_name)
            if "*" in role.permissions:
                return True
            return required_permission in role.permissions
        except ValueError:
            return False

    @staticmethod
    def get_role_permissions(role_name: str) -> Set[str]:
        try:
            role = RoleMatrix.get_role(role_name)
            return role.permissions
        except ValueError:
            return set()
