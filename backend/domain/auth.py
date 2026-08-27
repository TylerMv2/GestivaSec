"""
Gestiva Security (GestivaSec V1) — SLICE-001: Login Domain Model
Encapsulates User Identity, Password Verification (Bcrypt Direct), and JWT Access Tokens.
Enforces BR-04 (Multi-Tenant Organization Boundary).
"""
import uuid
import bcrypt
import jwt
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timedelta

from backend.config.settings import settings

@dataclass
class UserIdentity:
    id: str
    organization_id: str
    email: str
    password_hash: str
    role: str
    is_active: bool = True
    created_at: Optional[datetime] = None

    def verify_password(self, plain_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), self.password_hash.encode('utf-8'))

    def generate_access_token(self) -> str:
        payload = {
            "sub": self.id,
            "org_id": self.organization_id,
            "email": self.email,
            "role": self.role,
            "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
        }
        return jwt.encode(payload, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

    @staticmethod
    def hash_password(plain_password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(plain_password.encode('utf-8'), salt).decode('utf-8')
