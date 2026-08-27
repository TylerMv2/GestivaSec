"""
Gestiva Security (GestivaSec V1) — IAM-USERS: User Management Domain Model (CAP-01)
Encapsulates User Aggregate, Role Assignment, and Multi-Tenant Isolation (BR-04).
"""
import re
import uuid
import bcrypt
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

VALID_ROLES = {"SOC_ADMIN", "SOC_ANALYST", "SOC_OPERATOR", "AUDITOR"}

@dataclass
class User:
    id: Optional[str]
    organization_id: str
    email: str
    password_hash: str
    role: str
    is_active: bool = True
    created_at: Optional[datetime] = None

    def __post_init__(self):
        self.validate()
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.utcnow()

    def validate(self) -> None:
        if not self.organization_id or not self.organization_id.strip():
            raise ValueError("BR-04 Violation: Organization ID is required.")
        if not self.email or not self.email.strip():
            raise ValueError("El correo electrónico es obligatorio.")
        email_regex = r"^[^@]+@[^@]+\.[^@]+$"
        if not re.match(email_regex, self.email.strip()):
            raise ValueError("Formato de correo electrónico inválido.")
        if self.role not in VALID_ROLES:
            raise ValueError(f"Rol '{self.role}' inválido. Roles autorizados: {VALID_ROLES}")

    @staticmethod
    def hash_password(plain_password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')
