"""
Gestiva Security (GestivaSec V1) — Organization Application Service (SLICE-002)
Orchestrates Organization creation, retrieval, and switching.
"""
from typing import List, Optional
from backend.domain.organization import Organization
from backend.infrastructure.organization_repository import OrganizationRepository

class OrganizationApplicationService:
    def __init__(self, repo: Optional[OrganizationRepository] = None):
        self.repo = repo or OrganizationRepository()

    async def create_organization(self, name: str) -> Organization:
        slug = Organization.generate_slug(name)
        existing = await self.repo.get_by_slug(slug)
        if existing:
            raise ValueError(f"Ya existe una Organización registrada con el slug '{slug}'.")

        org = Organization(id=None, name=name, slug=slug)
        return await self.repo.create(org)

    async def list_organizations(self) -> List[Organization]:
        return await self.repo.list_all()

    async def get_organization(self, org_id: str) -> Optional[Organization]:
        return await self.repo.get_by_id(org_id)
