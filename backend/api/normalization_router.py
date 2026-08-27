"""
Gestiva Security (GestivaSec V1) — SPRINT 5: Event Normalization REST API Router
Exposes POST /api/v1/normalization/normalize and GET /api/v1/normalization/events.
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field

from backend.domain.collector import RawEventRecord
from backend.application.normalization_service import EventNormalizationService

router = APIRouter(prefix="/api/v1/normalization", tags=["Event Normalization Engine"])
normalization_service = EventNormalizationService()

class NormalizeRawRequest(BaseModel):
    collector_type: str = Field("SYSLOG", json_schema_extra={"example": "SYSLOG"})
    source_ip: str = Field("192.168.1.100", json_schema_extra={"example": "192.168.1.100"})
    source_hostname: Optional[str] = Field("syslog-gw", json_schema_extra={"example": "syslog-gw"})
    payload: Dict[str, Any] = Field(default_factory=dict)

class ObserverDTO(BaseModel):
    collector_id: str
    collector_type: str
    ip_address: str

class SourceDTO(BaseModel):
    ip: str
    hostname: Optional[str]
    geo_country: str
    geo_city: str
    geo_asn: str

class DestinationDTO(BaseModel):
    ip: str
    asset_id: Optional[str]

class ClassificationDTO(BaseModel):
    category: str
    action: str
    severity: str
    outcome: str
    protocol: str

class NormalizedEventDTO(BaseModel):
    event_id: str
    organization_id: str
    timestamp: str
    observer: ObserverDTO
    source: SourceDTO
    destination: DestinationDTO
    event: ClassificationDTO
    enrichment: Dict[str, Any] = Field(default_factory=dict)
    raw_event_id: Optional[str]

@router.post("/normalize", response_model=NormalizedEventDTO)
async def normalize_raw_event(
    payload: NormalizeRawRequest,
    x_organization_id: Optional[str] = Header(None)
):
    """Normalizes raw input into GestivaSec Event Schema (GES)."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    raw_record = RawEventRecord(
        organization_id=org_id,
        collector_type=payload.collector_type,
        source_ip=payload.source_ip,
        source_hostname=payload.source_hostname,
        payload=payload.payload
    )

    norm = await normalization_service.normalize_raw_event(raw_record)

    return NormalizedEventDTO(
        event_id=norm.event_id,
        organization_id=norm.organization_id,
        timestamp=norm.timestamp.isoformat(),
        observer=ObserverDTO(
            collector_id=norm.observer.collector_id,
            collector_type=norm.observer.collector_type,
            ip_address=norm.observer.ip_address
        ),
        source=SourceDTO(
            ip=norm.source.ip,
            hostname=norm.source.hostname,
            geo_country=norm.source.geo_country,
            geo_city=norm.source.geo_city,
            geo_asn=norm.source.geo_asn
        ),
        destination=DestinationDTO(
            ip=norm.destination.ip,
            asset_id=norm.destination.asset_id
        ),
        event=ClassificationDTO(
            category=norm.event.category,
            action=norm.event.action,
            severity=norm.event.severity,
            outcome=norm.event.outcome,
            protocol=norm.event.protocol
        ),
        enrichment=norm.enrichment,
        raw_event_id=norm.raw_event_id
    )

@router.get("/events", response_model=List[NormalizedEventDTO])
async def list_normalized_events(
    limit: int = 50,
    x_organization_id: Optional[str] = Header(None)
):
    """Returns normalized events formatted in GestivaSec Event Schema (GES)."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    events = await normalization_service.list_normalized_events(org_id, limit)
    return [
        NormalizedEventDTO(
            event_id=e.event_id,
            organization_id=e.organization_id,
            timestamp=e.timestamp.isoformat(),
            observer=ObserverDTO(
                collector_id=e.observer.collector_id,
                collector_type=e.observer.collector_type,
                ip_address=e.observer.ip_address
            ),
            source=SourceDTO(
                ip=e.source.ip,
                hostname=e.source.hostname,
                geo_country=e.source.geo_country,
                geo_city=e.source.geo_city,
                geo_asn=e.source.geo_asn
            ),
            destination=DestinationDTO(
                ip=e.destination.ip,
                asset_id=e.destination.asset_id
            ),
            event=ClassificationDTO(
                category=e.event.category,
                action=e.event.action,
                severity=e.event.severity,
                outcome=e.event.outcome,
                protocol=e.event.protocol
            ),
            enrichment=e.enrichment,
            raw_event_id=e.raw_event_id
        ) for e in events
    ]
