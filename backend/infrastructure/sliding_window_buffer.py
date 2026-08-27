"""
Gestiva Security (GestivaSec V1) — Sliding Time-Window Buffer Component
Buffers findings per Asset UUID within temporal sliding windows for multi-event correlation.
"""
import time
from datetime import datetime, timezone, timedelta
from typing import List, Dict, Any, Optional
from backend.domain.detection_rule import Finding

class SlidingWindowBuffer:
    def __init__(self, window_minutes: int = 15):
        self.window_minutes = window_minutes
        self._buffer: List[Dict[str, Any]] = []

    def add_finding(self, finding: Finding):
        """Pushes a finding into the sliding buffer."""
        self._buffer.append({
            "finding": finding,
            "timestamp": datetime.now(timezone.utc)
        })
        self.cleanup_expired()

    def cleanup_expired(self):
        """Removes findings older than window_minutes."""
        cutoff = datetime.now(timezone.utc) - timedelta(minutes=self.window_minutes)
        self._buffer = [f for f in self._buffer if f["timestamp"] >= cutoff]

    def get_findings_for_asset(self, asset_id: Optional[str], source_ip: str) -> List[Finding]:
        """Returns active findings for target asset within current sliding window."""
        self.cleanup_expired()
        results = []
        for entry in self._buffer:
            f: Finding = entry["finding"]
            if (asset_id and f.asset_id == asset_id) or (f.source_ip == source_ip):
                results.append(f)
        return results
