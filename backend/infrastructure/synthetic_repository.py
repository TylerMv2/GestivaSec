"""
Gestiva Security (GestivaSec V1) — Synthetic Observations & Telemetry Evidence Repository
In-memory & DB persistence for synthetic observations and telemetry evidence.
"""
from typing import List
from datetime import datetime
from backend.domain.synthetic import SyntheticObservation, TelemetryEvidence

class SyntheticRepository:
    _observations: List[SyntheticObservation] = []
    _evidences: List[TelemetryEvidence] = []

    def __init__(self):
        if not self._observations:
            default_org = "00000000-0000-0000-0000-000000000001"
            now = datetime.utcnow()
            self._observations.extend([
                SyntheticObservation(
                    id="obs-init-11111111",
                    organization_id=default_org,
                    asset_id="11111111-1111-1111-1111-111111111111",
                    target_url="https://gestivaone.com",
                    status_code=200,
                    latency_ms=14.5,
                    is_successful=True,
                    timestamp=now
                ),
                SyntheticObservation(
                    id="obs-init-22222222",
                    organization_id=default_org,
                    asset_id="22222222-2222-2222-2222-222222222222",
                    target_url="https://pay.gestivaone.com",
                    status_code=200,
                    latency_ms=18.2,
                    is_successful=True,
                    timestamp=now
                )
            ])

    async def save_observation(self, obs: SyntheticObservation) -> SyntheticObservation:
        self._observations.append(obs)
        return obs

    async def save_evidence(self, evidence: TelemetryEvidence) -> TelemetryEvidence:
        self._evidences.append(evidence)
        return evidence

    async def get_recent_failures_count(self, asset_id: str, limit: int = 3) -> int:
        asset_obs = [o for o in self._observations if o.asset_id == asset_id]
        if not asset_obs:
            return 0
        recent = sorted(asset_obs, key=lambda x: x.timestamp, reverse=True)[:limit]
        return sum(1 for o in recent if not o.is_successful)

    async def list_observations(self, organization_id: str) -> List[SyntheticObservation]:
        return [o for o in self._observations if o.organization_id == organization_id]

    async def list_evidences(self, organization_id: str) -> List[TelemetryEvidence]:
        return [e for e in self._evidences if e.organization_id == organization_id]
