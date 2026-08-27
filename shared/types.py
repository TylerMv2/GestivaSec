"""
Gestiva Security (GestivaSec V1) — Shared Kernel Type Definitions
"""
from typing import TypedDict, Optional, List
from datetime import datetime

class TenantContext(TypedDict):
    tenant_id: str
    organization_name: str
    is_active: bool

class UserContext(TypedDict):
    user_id: str
    email: str
    tenant_id: str
    role: str

class SyntheticEvaluationResult(TypedDict):
    asset_id: str
    target_url: str
    status_code: int
    latency_ms: float
    is_successful: bool
    timestamp: datetime
    error_message: Optional[str]
