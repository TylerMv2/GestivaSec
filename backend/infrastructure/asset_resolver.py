"""
Gestiva Security (GestivaSec V1) — Asset Resolver Infrastructure Component
Resolves event source IP address / hostname / MAC to an official Asset UUID from Asset Inventory.
"""
from typing import Optional
from backend.infrastructure.asset_repository import AssetRepository

class AssetResolver:
    def __init__(self, asset_repo: Optional[AssetRepository] = None):
        self.asset_repo = asset_repo or AssetRepository()

    async def resolve_asset_id(self, source_ip: str, organization_id: str, hostname: Optional[str] = None) -> Optional[str]:
        """Resolves source_ip or hostname against organization assets (BR-0004)."""
        assets = await self.asset_repo.list_by_organization(organization_id)
        
        # 1. Match by target_url / IP
        for asset in assets:
            if source_ip in asset.target_url or asset.target_url.endswith(source_ip):
                return asset.id

        # 2. Match by hostname
        if hostname:
            for asset in assets:
                if hostname.lower() in asset.name.lower():
                    return asset.id

        # 3. Match in historical IP history
        for asset in assets:
            for rec in asset.ip_history:
                if source_ip in rec.ip_address:
                    return asset.id

        return None
