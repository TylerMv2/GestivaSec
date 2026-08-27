"""
Gestiva Security (GestivaSec V1) — IAM-USERS: User Repository Persistence Adapter
"""
from typing import List, Optional
from backend.domain.user import User

class UserRepository:
    _users: List[User] = []

    def __init__(self):
        if not self._users:
            admin = User(
                id="00000000-0000-0000-0000-000000000099",
                organization_id="00000000-0000-0000-0000-000000000001",
                email="admin@gestivaone.com",
                password_hash=User.hash_password("GestivaSec2026!"),
                role="SOC_ADMIN",
                is_active=True
            )
            self._users.append(admin)

    async def create(self, user: User) -> User:
        self._users.append(user)
        return user

    async def get_by_email(self, email: str) -> Optional[User]:
        for u in self._users:
            if u.email.lower() == email.lower():
                return u
        return None

    async def get_by_id(self, user_id: str) -> Optional[User]:
        for u in self._users:
            if u.id == user_id:
                return u
        return None

    async def list_by_organization(self, organization_id: str) -> List[User]:
        return [u for u in self._users if u.organization_id == organization_id]
