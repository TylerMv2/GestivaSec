"""
Gestiva Security (GestivaSec V1) — Auth Repository Persistence Adapter (SLICE-001)
"""
from typing import List, Optional
from backend.domain.auth import UserIdentity

class AuthRepository:
    _users: List[UserIdentity] = []

    def __init__(self):
        if not self._users:
            # Seed default admin user (admin@gestivaone.com / GestivaSec2026!)
            admin = UserIdentity(
                id="00000000-0000-0000-0000-000000000099",
                organization_id="00000000-0000-0000-0000-000000000001",
                email="admin@gestivaone.com",
                password_hash=UserIdentity.hash_password("GestivaSec2026!"),
                role="SOC_ADMIN",
                is_active=True
            )
            self._users.append(admin)

    async def get_by_email(self, email: str) -> Optional[UserIdentity]:
        for user in self._users:
            if user.email.lower() == email.lower():
                return user
        return None

    async def get_by_id(self, user_id: str) -> Optional[UserIdentity]:
        for user in self._users:
            if user.id == user_id:
                return user
        return None
