"""
Gestiva Security (GestivaSec V1) — STAGE 11: Enterprise Reporting & Audit Export Domain Models
Pure domain models for Report Templates, Generated Report Jobs, Audit Export Requests, and Security Metrics Summaries.
"""
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional

class ReportType:
    EXECUTIVE_SUMMARY = "EXECUTIVE_SUMMARY"
    SOC_METRICS = "SOC_METRICS"
    INCIDENT_SUMMARY = "INCIDENT_SUMMARY"
    AUDIT_COMPLIANCE = "AUDIT_COMPLIANCE"
    THREAT_INTEL_SUMMARY = "THREAT_INTEL_SUMMARY"
    ASSET_INVENTORY = "ASSET_INVENTORY"

class ReportFormat:
    PDF = "PDF"
    CSV = "CSV"
    JSON = "JSON"

class JobStatus:
    QUEUED = "QUEUED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

@dataclass
class ReportTemplate:
    template_id: str = field(default_factory=lambda: f"TMPL-{uuid.uuid4().hex[:8].upper()}")
    name: str = "Executive SOC Security Summary"
    report_type: str = ReportType.EXECUTIVE_SUMMARY
    format: str = ReportFormat.PDF
    description: str = "High-level executive security posture and SOC metrics report."
    sections: List[str] = field(default_factory=lambda: ["EXECUTIVE_OVERVIEW", "INCIDENT_TRENDS", "THREAT_INTEL_SUMMARY", "ASSET_HEALTH"])
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class ReportJob:
    job_id: str = field(default_factory=lambda: f"JOB-{uuid.uuid4().hex[:8].upper()}")
    organization_id: str = "00000000-0000-0000-0000-000000000001"
    template_id: str = ""
    title: str = "Executive SOC Security Summary"
    report_type: str = ReportType.EXECUTIVE_SUMMARY
    format: str = ReportFormat.PDF
    status: str = JobStatus.COMPLETED
    parameters: Dict[str, Any] = field(default_factory=dict)
    schedule_cron: Optional[str] = None
    file_name: str = ""
    file_content: str = ""
    file_size_bytes: int = 0
    generated_by: str = "analyst@gestivaone.com"
    generated_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

@dataclass
class AuditExportRequest:
    export_id: str = field(default_factory=lambda: f"EXP-{uuid.uuid4().hex[:8].upper()}")
    organization_id: str = "00000000-0000-0000-0000-000000000001"
    format: str = ReportFormat.CSV
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    total_events_exported: int = 0
    status: str = JobStatus.COMPLETED
    file_content: str = ""
    requested_by: str = "soc-admin@gestivaone.com"
    requested_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))
