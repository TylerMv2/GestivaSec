"""
Gestiva Security (GestivaSec V1) — SLICE-007: Session & Invalidation Domain Model
Encapsulates User Session Tracking and Token Invalidation Blacklist (BR-0005).
"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Optional, Set

_TOKEN_BLACKLIST: Set[str] = set()

def revoke_token(token: str) -> None:
    """Adds token to revoked blacklist."""
    _TOKEN_BLACKLIST.add(token)

def is_token_revoked(token: str) -> bool:
    """Checks if token is present in blacklist."""
    return token in _TOKEN_BLACKLIST

def clear_blacklist() -> None:
    """Clears blacklist (used for test setup/teardown)."""
    _TOKEN_BLACKLIST.clear()

@dataclass
class UserSession:
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str = ""
    organization_id: str = ""
    token: str = ""
    ip_address: str = "127.0.0.1"
    user_agent: str = "Internal/1.0"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
    is_active: bool = True

    def invalidate(self) -> None:
        """Invalidates current session and revokes its associated JWT token."""
        self.is_active = False
        if self.token:
            revoke_token(self.token)
