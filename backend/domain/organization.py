"""
Gestiva Security (GestivaSec V1) — SLICE-002: Organizations Domain Model
Encapsulates Organization Aggregate, Multi-Tenant Boundary (BR-04), and Tenant Status.
"""
import re
import uuid
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Organization:
    id: Optional[str]
    name: str
    slug: str
    status: str = "ACTIVE_ORGANIZATION"
    created_at: Optional[datetime] = None

    def __post_init__(self):
        self.validate()
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.slug:
            self.slug = self.generate_slug(self.name)
        if not self.created_at:
            self.created_at = datetime.utcnow()

    def validate(self) -> None:
        """Enforces domain validation for organization."""
        if not self.name or not self.name.strip():
            raise ValueError("El nombre de la Organización no puede estar vacío.")
        if len(self.name.strip()) < 3:
            raise ValueError("El nombre de la Organización debe tener al menos 3 caracteres.")

    @staticmethod
    def generate_slug(name: str) -> str:
        slug = re.sub(r'[^a-zA-Z0-9\s-]', '', name.lower())
        return re.sub(r'[\s-]+', '-', slug).strip('-')
