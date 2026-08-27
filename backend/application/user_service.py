"""
Gestiva Security (GestivaSec V1) — IAM-USERS: User Management Application Service
Orchestrates User Registration, Email Uniqueness, and Role Assignments.
"""
from typing import List, Optional
from backend.domain.user import User
from backend.infrastructure.user_repository import UserRepository

class UserApplicationService:
    def __init__(self, repo: Optional[UserRepository] = None):
        self.repo = repo or UserRepository()

    async def register_user(
        self,
        organization_id: str,
        email: str,
        plain_password: str,
        role: str = "SOC_ANALYST"
    ) -> User:
        existing = await self.repo.get_by_email(email)
        if existing:
            raise ValueError(f"Ya existe un usuario registrado con el correo '{email}'.")

        password_hash = User.hash_password(plain_password)
        user = User(
            id=None,
            organization_id=organization_id,
            email=email,
            password_hash=password_hash,
            role=role,
            is_active=True
        )
        return await self.repo.create(user)

    async def list_users(self, organization_id: str) -> List[User]:
        return await self.repo.list_by_organization(organization_id)

    async def get_user(self, user_id: str) -> Optional[User]:
        return await self.repo.get_by_id(user_id)
