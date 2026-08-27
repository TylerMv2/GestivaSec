"""
Gestiva Security (GestivaSec V1) — Distributed Continuous Monitoring Scheduler Domain Model
Encapsulates 1m (HTTP/HTTPS/Latency), 5m (DNS/MX/TXT/SPF/DKIM/DMARC), and 1h (TLS/Cipher/SAN) Jobs + Change Store.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class JobInterval(str, Enum):
    EVERY_MINUTE = "1m"
    EVERY_FIVE_MINUTES = "5m"
    EVERY_HOUR = "1h"

@dataclass
class HttpAuditResult:
    target_url: str
    is_available: bool
    status_code: int
    latency_ms: float
    response_time_sec: float

@dataclass
class DnsAuditResult:
    domain: str
    mx_records: List[str]
    txt_records: List[str]
    has_spf: bool
    has_dkim: bool
    has_dmarc: bool

@dataclass
class TlsAuditResult:
    domain: str
    tls_version: str
    cipher_suite: str
    days_to_expiration: int
    san_list: List[str]

@dataclass
class ChangeLogEntry:
    target_url: str
    change_category: str  # "HTTP_STATE", "DNS_RECORD", "TLS_CERTIFICATE"
    property_name: str
    old_value: str
    new_value: str
    detected_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class JobExecutionLog:
    job_id: str
    target_url: str
    job_type: str
    executed_at: datetime
    success: bool
    details: str

@dataclass
class SOCScheduleJob:
    job_id: str
    target_asset_id: str
    target_url: str
    interval: JobInterval
    job_type: str
    last_run_at: Optional[datetime] = None
    status: str = "SCHEDULED"
