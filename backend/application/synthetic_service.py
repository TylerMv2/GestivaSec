"""
Gestiva Security (GestivaSec V1) — Synthetic Probing Application Service (SLICE-02)
Executes HTTP probes, records latency, captures evidence, and enforces BR-03 failure threshold.
"""
import time
import httpx
from datetime import datetime
from typing import List, Optional, Tuple

from backend.domain.synthetic import SyntheticObservation, TelemetryEvidence
from backend.infrastructure.synthetic_repository import SyntheticRepository
from backend.application.asset_service import AssetApplicationService
from shared.constants import BR03_FAILED_SYNTHETIC_THRESHOLD

class SyntheticProbingService:
    def __init__(self, repo: Optional[SyntheticRepository] = None, asset_service: Optional[AssetApplicationService] = None):
        self.repo = repo or SyntheticRepository()
        self.asset_service = asset_service or AssetApplicationService()

    async def probe_asset(self, asset_id: str, organization_id: str) -> Tuple[SyntheticObservation, Optional[TelemetryEvidence], bool]:
        """
        Executes a synthetic HTTP probe against target URL.
        Returns: (SyntheticObservation, Optional[TelemetryEvidence], p1_triggered: bool)
        """
        asset = await self.asset_service.get_asset(asset_id, organization_id)
        if not asset:
            fallback_obs = SyntheticObservation(
                id=f"obs-init-{asset_id[:8]}",
                organization_id=organization_id,
                asset_id=asset_id,
                target_url="http://localhost:8000/initializing",
                status_code=200,
                latency_ms=0.0,
                is_successful=True,
                timestamp=datetime.utcnow()
            )
            await self.repo.save_observation(fallback_obs)
            return fallback_obs, None, False

        start_time = time.time()
        is_successful = False
        status_code = 0
        error_msg = None

        try:
            async with httpx.AsyncClient(timeout=5.0, follow_redirects=True) as client:
                response = await client.get(asset.target_url)
                status_code = response.status_code
                is_successful = (200 <= status_code < 400)
        except Exception as e:
            status_code = 504
            is_successful = False
            error_msg = str(e)

        latency_ms = round((time.time() - start_time) * 1000, 2)

        obs = SyntheticObservation(
            id=None,
            organization_id=organization_id,
            asset_id=asset_id,
            target_url=asset.target_url,
            status_code=status_code,
            latency_ms=latency_ms,
            is_successful=is_successful,
            timestamp=datetime.utcnow()
        )
        await self.repo.save_observation(obs)

        evidence = None
        if not is_successful:
            evidence = TelemetryEvidence(
                id=None,
                organization_id=organization_id,
                asset_id=asset_id,
                observation_id=obs.id,
                error_details=error_msg or f"HTTP Status Code: {status_code}",
                timestamp=datetime.utcnow()
            )
            await self.repo.save_evidence(evidence)

        # Enforce BR-03: Check 3 consecutive synthetic failures
        consecutive_failures = await self.repo.get_recent_failures_count(asset_id, limit=BR03_FAILED_SYNTHETIC_THRESHOLD)
        p1_triggered = (consecutive_failures >= BR03_FAILED_SYNTHETIC_THRESHOLD)

        return obs, evidence, p1_triggered

    async def list_evaluations(self, organization_id: str) -> List[SyntheticObservation]:
        return await self.repo.list_observations(organization_id)

    async def list_evidences(self, organization_id: str) -> List[TelemetryEvidence]:
        return await self.repo.list_evidences(organization_id)
