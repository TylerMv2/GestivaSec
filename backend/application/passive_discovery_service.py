"""
Gestiva Security (GestivaSec V1) — Passive Discovery Application Service
Orchestrates Continuous Passive Security Observability for GestivaOne assets.
"""
from typing import Dict, List, Optional
from backend.domain.passive_discovery import PassiveDiscoveryReport
from backend.infrastructure.passive_discovery_engine import PassiveDiscoveryEngine

class PassiveDiscoveryService:
    _reports: Dict[str, PassiveDiscoveryReport] = {}

    async def scan_asset(self, asset_id: str, target_url: str) -> PassiveDiscoveryReport:
        report = await PassiveDiscoveryEngine.run_passive_scan(asset_id, target_url)
        self._reports[asset_id] = report
        return report

    async def get_report(self, asset_id: str) -> Optional[PassiveDiscoveryReport]:
        return self._reports.get(asset_id)

    async def list_all_reports(self) -> List[PassiveDiscoveryReport]:
        return list(self._reports.values())
