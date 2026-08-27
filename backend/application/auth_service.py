"""
Gestiva Security (GestivaSec V1) — Authentication Application Service (SLICE-001 & SLICE-007)
Orchestrates User Login, Credentials Verification, JWT Token Issuance, and Session Blacklist Invalidation (BR-0005).
"""
import jwt
from typing import Optional, Tuple
from backend.domain.auth import UserIdentity
from backend.domain.session import is_token_revoked, revoke_token
from backend.infrastructure.auth_repository import AuthRepository
from backend.config.settings import settings

class AuthenticationService:
    def __init__(self, repo: Optional[AuthRepository] = None):
        self.repo = repo or AuthRepository()

    async def authenticate_user(self, email: str, plain_password: str) -> Tuple[UserIdentity, str]:
        user = await self.repo.get_by_email(email)
        if not user or not user.is_active:
            raise ValueError("Credenciales inválidas o cuenta inactiva.")

        if not user.verify_password(plain_password):
            raise ValueError("Credenciales inválidas. Compruebe correo y contraseña.")

        token = user.generate_access_token()
        return user, token

    async def verify_token(self, token: str) -> Optional[UserIdentity]:
        if is_token_revoked(token):
            return None

        try:
            payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
            user_id = payload.get("sub")
            if not user_id:
                return None
            return await self.repo.get_by_id(user_id)
        except Exception:
            return None

    async def revoke_token(self, token: str) -> bool:
        """Revokes token and adds it to the blacklist."""
        revoke_token(token)
        return True
