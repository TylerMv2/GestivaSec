"""
Gestiva Security (GestivaSec V1) — Digital Asset Application Service
Orchestrates Asset Registration and Management Use Cases.
"""
from typing import List, Optional
from backend.domain.asset import DigitalAsset
from backend.infrastructure.asset_repository import AssetRepository
from shared.constants import AssetStatus

class AssetApplicationService:
    def __init__(self, repository: Optional[AssetRepository] = None):
        self.repository = repository or AssetRepository()

    async def register_asset(
        self,
        organization_id: str,
        name: str,
        target_url: str,
        criticality: str,
        owner_email: str
    ) -> DigitalAsset:
        asset = DigitalAsset(
            id=None,
            organization_id=organization_id,
            name=name,
            target_url=target_url,
            criticality=criticality,
            owner_email=owner_email,
            status=AssetStatus.ACTIVE
        )
        return await self.repository.create(asset)

    async def list_assets(self, organization_id: str) -> List[DigitalAsset]:
        return await self.repository.list_by_organization(organization_id)

    async def get_asset(self, asset_id: str, organization_id: str) -> Optional[DigitalAsset]:
        return await self.repository.get_by_id(asset_id, organization_id)
