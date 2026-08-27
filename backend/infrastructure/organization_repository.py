"""
Gestiva Security (GestivaSec V1) — Organization Repository Persistence Adapter (SLICE-002)
"""
from typing import List, Optional
from backend.domain.organization import Organization

class OrganizationRepository:
    _orgs: List[Organization] = []

    def __init__(self):
        if not self._orgs:
            self._orgs.extend([
                Organization(
                    id="00000000-0000-0000-0000-000000000001",
                    name="GestivaOne Corporation",
                    slug="gestivaone-corp",
                    status="ACTIVE_ORGANIZATION"
                ),
                Organization(
                    id="00000000-0000-0000-0000-000000000002",
                    name="Festa Event Systems",
                    slug="festa-events",
                    status="ACTIVE_ORGANIZATION"
                )
            ])

    async def create(self, org: Organization) -> Organization:
        self._orgs.append(org)
        return org

    async def get_by_id(self, org_id: str) -> Optional[Organization]:
        for org in self._orgs:
            if org.id == org_id:
                return org
        return None

    async def get_by_slug(self, slug: str) -> Optional[Organization]:
        for org in self._orgs:
            if org.slug == slug:
                return org
        return None

    async def list_all(self) -> List[Organization]:
        return self._orgs
