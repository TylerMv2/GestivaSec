"""
Gestiva Security (GestivaSec V1) — SPRINT 4: Event Collectors REST API Router
Exposes POST /api/v1/collectors/ingest, GET /api/v1/collectors/events, and GET /api/v1/collectors/metrics.
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field

from backend.application.collector_service import CollectorManagerService
from backend.application.auth_service import AuthenticationService

router = APIRouter(prefix="/api/v1/collectors", tags=["Event Collectors Framework"])
collector_manager = CollectorManagerService()
auth_service = AuthenticationService()

class EventIngestRequest(BaseModel):
    collector_type: str = Field("SYSLOG", json_schema_extra={"example": "SYSLOG"})
    source_ip: str = Field("192.168.1.100", json_schema_extra={"example": "192.168.1.100"})
    source_hostname: Optional[str] = Field("syslog-gw", json_schema_extra={"example": "syslog-gw"})
    payload: Dict[str, Any] = Field(default_factory=dict)

class RawEventResponse(BaseModel):
    raw_event_id: str
    organization_id: str
    collector_type: str
    source_ip: str
    source_hostname: Optional[str]
    resolved_asset_id: Optional[str]
    payload: Dict[str, Any]
    received_at: str

class CollectorMetricsDTO(BaseModel):
    collector_type: str
    events_ingested: int
    events_per_second: float
    average_latency_ms: float
    dropped_events: int
    active: bool

@router.post("/ingest", response_model=RawEventResponse)
async def ingest_raw_event(
    payload: EventIngestRequest,
    x_organization_id: Optional[str] = Header(None)
):
    """High-throughput Event Ingestion Endpoint with Asset Resolver matching."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    raw_payload = payload.payload or {}
    raw_payload["source_ip"] = payload.source_ip
    if payload.source_hostname:
        raw_payload["hostname"] = payload.source_hostname

    record = await collector_manager.ingest_event(payload.collector_type, raw_payload, org_id)

    return RawEventResponse(
        raw_event_id=record.raw_event_id,
        organization_id=record.organization_id,
        collector_type=record.collector_type,
        source_ip=record.source_ip,
        source_hostname=record.source_hostname,
        resolved_asset_id=record.resolved_asset_id,
        payload=record.payload,
        received_at=record.received_at.isoformat()
    )

@router.get("/events", response_model=List[RawEventResponse])
async def list_raw_events(
    limit: int = 50,
    x_organization_id: Optional[str] = Header(None)
):
    """Returns ingested raw event log for tenant (BR-0004)."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    events = await collector_manager.list_raw_events(org_id, limit)
    return [
        RawEventResponse(
            raw_event_id=e.raw_event_id,
            organization_id=e.organization_id,
            collector_type=e.collector_type,
            source_ip=e.source_ip,
            source_hostname=e.source_hostname,
            resolved_asset_id=e.resolved_asset_id,
            payload=e.payload,
            received_at=e.received_at.isoformat()
        ) for e in events
    ]

@router.get("/metrics", response_model=List[CollectorMetricsDTO])
async def get_collector_metrics():
    """Returns live EPS and health metrics for all 5 collectors."""
    metrics = collector_manager.get_collector_metrics()
    return [
        CollectorMetricsDTO(
            collector_type=m.collector_type,
            events_ingested=m.events_ingested,
            events_per_second=m.events_per_second,
            average_latency_ms=m.average_latency_ms,
            dropped_events=m.dropped_events,
            active=m.active
        ) for m in metrics
    ]
