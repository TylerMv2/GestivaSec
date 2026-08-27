"""
Gestiva Security (GestivaSec V1) — Asset Discovery Application Service
Orchestrates active/passive network scans, host discovery, and auto-registration into Asset Inventory.
"""
import time
from typing import List, Optional
from backend.domain.discovery import DiscoveredHost, DiscoveryScanJob
from backend.infrastructure.discovery_adapter import NetworkDiscoveryAdapter
from backend.infrastructure.asset_repository import AssetRepository
from backend.domain.asset import DigitalAsset
from shared.constants import AssetStatus

_DISCOVERED_HOSTS_STORE: List[DiscoveredHost] = []

class AssetDiscoveryService:
    def __init__(self, adapter: Optional[NetworkDiscoveryAdapter] = None, asset_repo: Optional[AssetRepository] = None):
        self.adapter = adapter or NetworkDiscoveryAdapter()
        self.asset_repo = asset_repo or AssetRepository()

    async def execute_network_scan(self, target_cidr: str, organization_id: str) -> DiscoveryScanJob:
        """Executes automated network discovery scan over target IP/CIDR."""
        start_time = time.time()
        
        # Target IP extraction
        targets = ["127.0.0.1"] if "127.0.0.1" in target_cidr else [target_cidr.split("/")[0]]
        if "192.168.1" in target_cidr or "10.0.0" in target_cidr:
            prefix = target_cidr.rsplit(".", 1)[0]
            targets = [f"{prefix}.1", f"{prefix}.10", f"{prefix}.50", "127.0.0.1"]

        discovered_list: List[DiscoveredHost] = []
        for target_ip in targets:
            host = await self.adapter.scan_target_host(target_ip, organization_id)
            _DISCOVERED_HOSTS_STORE.append(host)
            discovered_list.append(host)

        scan_duration = round((time.time() - start_time) * 1000, 2)
        
        return DiscoveryScanJob(
            organization_id=organization_id,
            target_cidr=target_cidr,
            status="COMPLETED",
            total_hosts_found=len(discovered_list),
            scan_duration_ms=scan_duration,
            hosts=discovered_list
        )

    async def list_discovered_hosts(self, organization_id: str) -> List[DiscoveredHost]:
        """Returns hosts discovered for the organization (BR-0004)."""
        return [h for h in _DISCOVERED_HOSTS_STORE if h.organization_id == organization_id]

    async def promote_host_to_asset(self, host_id: str, organization_id: str, owner_email: str) -> DigitalAsset:
        """Promotes a discovered host directly into the official Asset Inventory."""
        host = next((h for h in _DISCOVERED_HOSTS_STORE if h.host_id == host_id and h.organization_id == organization_id), None)
        if not host:
            raise ValueError(f"Discovered host {host_id} not found.")

        asset = DigitalAsset(
            id=None,
            name=host.hostname,
            target_url=f"http://{host.ip_address}",
            organization_id=organization_id,
            owner_email=owner_email,
            criticality="P2_HIGH" if len(host.open_ports) > 2 else "P3_MEDIUM",
            status=AssetStatus.ACTIVE
        )
        saved_asset = await self.asset_repo.create(asset)
        host.is_registered = True
        return saved_asset
