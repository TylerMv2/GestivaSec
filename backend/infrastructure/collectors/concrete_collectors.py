"""
Gestiva Security (GestivaSec V1) — Concrete Event Collectors (SPRINT 4)
Implementations for Syslog RFC5424, Windows EVTX/JSON, Generic REST JSON, Cloud Webhooks, and Agent Event Stream.
"""
import time
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from backend.domain.collector import RawEventRecord
from backend.infrastructure.collectors.base_collector import BaseCollector

class SyslogCollector(BaseCollector):
    def __init__(self):
        super().__init__(collector_type="SYSLOG")

    async def process_raw_payload(self, payload: Dict[str, Any], organization_id: str) -> RawEventRecord:
        source_ip = payload.get("source_ip", "192.168.1.100")
        hostname = payload.get("hostname", "syslog-gateway")
        asset_id = await self.asset_resolver.resolve_asset_id(source_ip, organization_id, hostname)

        self.events_ingested += 1
        self.last_event_time = datetime.now(timezone.utc)

        return RawEventRecord(
            organization_id=organization_id,
            collector_type=self.collector_type,
            source_ip=source_ip,
            source_hostname=hostname,
            resolved_asset_id=asset_id,
            payload={
                "facility": payload.get("facility", 1),
                "severity": payload.get("severity", 3),
                "message": payload.get("message", "Syslog auth failure detected"),
                "raw_text": payload.get("raw_text", f"<34>1 {datetime.now(timezone.utc).isoformat()} {hostname} sshd - - Failed password")
            }
        )

class WindowsEventCollector(BaseCollector):
    def __init__(self):
        super().__init__(collector_type="WINDOWS_EVTX")

    async def process_raw_payload(self, payload: Dict[str, Any], organization_id: str) -> RawEventRecord:
        source_ip = payload.get("source_ip", "10.0.0.15")
        hostname = payload.get("computer_name", "DC-01.gestivaone.internal")
        asset_id = await self.asset_resolver.resolve_asset_id(source_ip, organization_id, hostname)

        self.events_ingested += 1
        self.last_event_time = datetime.now(timezone.utc)

        return RawEventRecord(
            organization_id=organization_id,
            collector_type=self.collector_type,
            source_ip=source_ip,
            source_hostname=hostname,
            resolved_asset_id=asset_id,
            payload={
                "event_id": payload.get("event_id", 4625),
                "channel": payload.get("channel", "Security"),
                "provider_name": "Microsoft-Windows-Security-Auditing",
                "task_name": "Logon",
                "target_user_name": payload.get("target_user_name", "Administrator"),
                "logon_type": payload.get("logon_type", 3),
                "status_code": "0xC000006D"
            }
        )

class JsonCollector(BaseCollector):
    def __init__(self):
        super().__init__(collector_type="REST_JSON")

    async def process_raw_payload(self, payload: Dict[str, Any], organization_id: str) -> RawEventRecord:
        source_ip = payload.get("source_ip", "127.0.0.1")
        hostname = payload.get("hostname")
        asset_id = await self.asset_resolver.resolve_asset_id(source_ip, organization_id, hostname)

        self.events_ingested += 1
        self.last_event_time = datetime.now(timezone.utc)

        return RawEventRecord(
            organization_id=organization_id,
            collector_type=self.collector_type,
            source_ip=source_ip,
            source_hostname=hostname,
            resolved_asset_id=asset_id,
            payload=payload
        )

class WebhookCollector(BaseCollector):
    def __init__(self):
        super().__init__(collector_type="CLOUD_WEBHOOK")

    async def process_raw_payload(self, payload: Dict[str, Any], organization_id: str) -> RawEventRecord:
        source_ip = payload.get("source_ip", "52.94.233.12") # AWS / Cloud IP
        hostname = payload.get("provider", "aws-cloudtrail")
        asset_id = await self.asset_resolver.resolve_asset_id(source_ip, organization_id, hostname)

        self.events_ingested += 1
        self.last_event_time = datetime.now(timezone.utc)

        return RawEventRecord(
            organization_id=organization_id,
            collector_type=self.collector_type,
            source_ip=source_ip,
            source_hostname=hostname,
            resolved_asset_id=asset_id,
            payload=payload
        )

class AgentCollector(BaseCollector):
    def __init__(self):
        super().__init__(collector_type="GESTIVASEC_AGENT")

    async def process_raw_payload(self, payload: Dict[str, Any], organization_id: str) -> RawEventRecord:
        source_ip = payload.get("agent_ip", "192.168.1.50")
        hostname = payload.get("agent_hostname", "agent-linux-node")
        asset_id = await self.asset_resolver.resolve_asset_id(source_ip, organization_id, hostname)

        self.events_ingested += 1
        self.last_event_time = datetime.now(timezone.utc)

        return RawEventRecord(
            organization_id=organization_id,
            collector_type=self.collector_type,
            source_ip=source_ip,
            source_hostname=hostname,
            resolved_asset_id=asset_id,
            payload=payload
        )
