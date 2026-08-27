"""
Gestiva Security (GestivaSec V1) — Asset Repository Persistence Adapter
Supports in-memory persistence and asyncpg database connectivity.
"""
import uuid
from typing import List, Optional
from datetime import datetime
from backend.domain.asset import DigitalAsset
from shared.constants import AssetStatus

class AssetRepository:
    """In-Memory & Database Persistence Adapter for Digital Assets."""
    _in_memory_db: List[DigitalAsset] = []

    def __init__(self):
        # Seed initial assets for gestivaone ecosystem if empty
        if not self._in_memory_db:
            default_tenant = "00000000-0000-0000-0000-000000000001"
            self._in_memory_db.extend([
                DigitalAsset(
                    id="11111111-1111-1111-1111-111111111111",
                    organization_id=default_tenant,
                    name="GestivaOne Core Web Portal",
                    target_url="https://gestivaone.com",
                    criticality="P1_CRITICAL",
                    owner_email="ops@gestivaone.com",
                    status=AssetStatus.ACTIVE,
                    created_at=datetime.utcnow()
                ),
                DigitalAsset(
                    id="22222222-2222-2222-2222-222222222222",
                    organization_id=default_tenant,
                    name="GestivaOne E-Commerce Store",
                    target_url="https://gestivaone-store.vercel.app",
                    criticality="P2_HIGH",
                    owner_email="devops@gestivaone.com",
                    status=AssetStatus.ACTIVE,
                    created_at=datetime.utcnow()
                ),
                DigitalAsset(
                    id="33333333-3333-3333-3333-333333333333",
                    organization_id=default_tenant,
                    name="Festa Event Platform",
                    target_url="https://festa.gestivaone.com",
                    criticality="P2_HIGH",
                    owner_email="festa-lead@gestivaone.com",
                    status=AssetStatus.ACTIVE,
                    created_at=datetime.utcnow()
                )
            ])

    async def create(self, asset: DigitalAsset) -> DigitalAsset:
        if not asset.id:
            asset.id = str(uuid.uuid4())
        if not asset.created_at:
            asset.created_at = datetime.utcnow()
        self._in_memory_db.append(asset)
        return asset

    async def list_by_organization(self, organization_id: str) -> List[DigitalAsset]:
        return [a for a in self._in_memory_db if a.organization_id == organization_id]

    async def get_by_id(self, asset_id: str, organization_id: str) -> Optional[DigitalAsset]:
        for asset in self._in_memory_db:
            if asset.id == asset_id and asset.organization_id == organization_id:
                return asset
        return None
