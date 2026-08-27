"""
Gestiva Security (GestivaSec V1) — IAM-ROLES: RBAC Roles & Permissions Matrix (CAP-01)
Defines Role Hierarchy and Granular Permission Mapping.
"""
from dataclasses import dataclass, field
from typing import List, Set

@dataclass
class RoleDefinition:
    name: str
    description: str
    permissions: Set[str] = field(default_factory=set)

class RoleMatrix:
    """Pre-defined Role & Permissions Matrix for GestivaSec V1."""
    ROLES = {
        "SOC_ADMIN": RoleDefinition(
            name="SOC_ADMIN",
            description="Administrador General de Seguridad y Operaciones SOC",
            permissions={"*"}
        ),
        "SOC_ANALYST": RoleDefinition(
            name="SOC_ANALYST",
            description="Analista de Seguridad SOC - Gestión de Activos, Evidencias e Incidentes",
            permissions={"assets:read", "assets:create", "synthetic:evaluate", "incidents:read", "incidents:update"}
        ),
        "SOC_OPERATOR": RoleDefinition(
            name="SOC_OPERATOR",
            description="Operador de Monitoreo - Ejecución de Sondeos y Visualización",
            permissions={"assets:read", "synthetic:evaluate", "incidents:read"}
        ),
        "AUDITOR": RoleDefinition(
            name="AUDITOR",
            description="Auditor de Cumplimiento - Lectura de Trazas de Auditoría e Invariantes",
            permissions={"assets:read", "audit:read", "rca:read"}
        )
    }

    @classmethod
    def get_role(cls, role_name: str) -> RoleDefinition:
        if role_name not in cls.ROLES:
            raise ValueError(f"Rol '{role_name}' no existe en la Matriz RBAC.")
        return cls.ROLES[role_name]

    @classmethod
    def list_roles(cls) -> List[RoleDefinition]:
        return list(cls.ROLES.values())
