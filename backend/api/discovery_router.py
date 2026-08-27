"""
Gestiva Security (GestivaSec V1) — SPRINT 2: Asset Discovery REST Router
Exposes POST /api/v1/discovery/scan, GET /api/v1/discovery/hosts, and POST /api/v1/discovery/promote.
"""
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Depends, Header
from pydantic import BaseModel, Field

from backend.application.discovery_service import AssetDiscoveryService
from backend.application.auth_service import AuthenticationService

router = APIRouter(prefix="/api/v1/discovery", tags=["Asset Discovery Engine"])
discovery_service = AssetDiscoveryService()
auth_service = AuthenticationService()

class DiscoveryScanRequest(BaseModel):
    target_cidr: str = Field("192.168.1.0/24", json_schema_extra={"example": "192.168.1.0/24"})

class PromoteHostRequest(BaseModel):
    host_id: str
    owner_email: str = "ops@gestivaone.com"

class PortDTO(BaseModel):
    port: int
    protocol: str
    service_name: str
    banner: str
    status: str

class DiscoveredHostDTO(BaseModel):
    host_id: str
    organization_id: str
    ip_address: str
    hostname: str
    os_family: str
    mac_address: str
    vendor: str
    latency_ms: float
    open_ports: List[PortDTO]
    discovery_method: str
    is_registered: bool

class DiscoveryScanJobDTO(BaseModel):
    job_id: str
    organization_id: str
    target_cidr: str
    status: str
    total_hosts_found: int
    scan_duration_ms: float
    hosts: List[DiscoveredHostDTO]

@router.post("/scan", response_model=DiscoveryScanJobDTO)
async def trigger_network_discovery_scan(
    payload: DiscoveryScanRequest,
    authorization: Optional[str] = Header(None),
    x_organization_id: Optional[str] = Header(None)
):
    """Triggers an automated network discovery scan over the specified CIDR range."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    job = await discovery_service.execute_network_scan(payload.target_cidr, org_id)

    return DiscoveryScanJobDTO(
        job_id=job.job_id,
        organization_id=job.organization_id,
        target_cidr=job.target_cidr,
        status=job.status,
        total_hosts_found=job.total_hosts_found,
        scan_duration_ms=job.scan_duration_ms,
        hosts=[
            DiscoveredHostDTO(
                host_id=h.host_id,
                organization_id=h.organization_id,
                ip_address=h.ip_address,
                hostname=h.hostname,
                os_family=h.os_family,
                mac_address=h.mac_address,
                vendor=h.vendor,
                latency_ms=h.latency_ms,
                open_ports=[
                    PortDTO(
                        port=p.port,
                        protocol=p.protocol,
                        service_name=p.service_name,
                        banner=p.banner,
                        status=p.status
                    ) for p in h.open_ports
                ],
                discovery_method=h.discovery_method,
                is_registered=h.is_registered
            ) for h in job.hosts
        ]
    )

@router.get("/hosts", response_model=List[DiscoveredHostDTO])
async def list_discovered_hosts(x_organization_id: Optional[str] = Header(None)):
    """Returns all network hosts discovered for the organization (BR-0004)."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    hosts = await discovery_service.list_discovered_hosts(org_id)

    return [
        DiscoveredHostDTO(
            host_id=h.host_id,
            organization_id=h.organization_id,
            ip_address=h.ip_address,
            hostname=h.hostname,
            os_family=h.os_family,
            mac_address=h.mac_address,
            vendor=h.vendor,
            latency_ms=h.latency_ms,
            open_ports=[
                PortDTO(
                    port=p.port,
                    protocol=p.protocol,
                    service_name=p.service_name,
                    banner=p.banner,
                    status=p.status
                ) for p in h.open_ports
            ],
            discovery_method=h.discovery_method,
            is_registered=h.is_registered
        ) for h in hosts
    ]

@router.post("/promote")
async def promote_host_to_asset(
    payload: PromoteHostRequest,
    x_organization_id: Optional[str] = Header(None)
):
    """Promotes a discovered host directly into the official Asset Inventory."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    try:
        asset = await discovery_service.promote_host_to_asset(payload.host_id, org_id, payload.owner_email)
        return {
            "status": "PROMOTED",
            "asset_id": asset.id,
            "name": asset.name,
            "target_url": asset.target_url
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
