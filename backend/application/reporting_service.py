"""
Gestiva Security (GestivaSec V1) — STAGE 11: Enterprise Reporting Application Service
Orchestrates Report Templates, Report Generation Jobs, Audit Export Requests, and Audit Logging.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from backend.domain.reporting import (
    ReportTemplate,
    ReportJob,
    AuditExportRequest,
    ReportType,
    ReportFormat,
    JobStatus
)
from backend.infrastructure.reporting_generator import ReportingGenerator
from backend.infrastructure.audit_repository import AuditRepository, AuditEvent

_DEFAULT_TEMPLATES: List[ReportTemplate] = [
    ReportTemplate(template_id="TMPL-EXEC-01", name="Executive SOC Security Summary", report_type=ReportType.EXECUTIVE_SUMMARY, format=ReportFormat.PDF, description="Executive-level SOC metrics, incident volume, threat landscape summary."),
    ReportTemplate(template_id="TMPL-METRICS-02", name="SOC Operational Performance & SLA Report", report_type=ReportType.SOC_METRICS, format=ReportFormat.CSV, description="Analyst triage metrics, mean time to respond (MTTR), SLA compliance."),
    ReportTemplate(template_id="TMPL-INCIDENT-03", name="Incident & Case Investigation Summary", report_type=ReportType.INCIDENT_SUMMARY, format=ReportFormat.JSON, description="Detailed incident timeline, evidence references, root cause analyses."),
    ReportTemplate(template_id="TMPL-AUDIT-04", name="Regulatory & Compliance Audit Trail", report_type=ReportType.AUDIT_COMPLIANCE, format=ReportFormat.CSV, description="Immutable system audit event logs for compliance export.")
]

_REPORT_JOBS_STORE: List[ReportJob] = []
_AUDIT_EXPORTS_STORE: List[AuditExportRequest] = []

class ReportingApplicationService:
    def __init__(self, generator: Optional[ReportingGenerator] = None, audit_repo: Optional[AuditRepository] = None):
        self.generator = generator or ReportingGenerator()
        self.audit_repo = audit_repo or AuditRepository()

    def list_templates(self) -> List[ReportTemplate]:
        return list(_DEFAULT_TEMPLATES)

    def get_template(self, template_id: str) -> Optional[ReportTemplate]:
        return next((t for t in _DEFAULT_TEMPLATES if t.template_id == template_id), None)

    async def generate_report(
        self,
        organization_id: str,
        template_id: str,
        title: Optional[str] = None,
        fmt: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
        generated_by: str = "analyst@gestivaone.com"
    ) -> ReportJob:
        tmpl = self.get_template(template_id)
        report_type = tmpl.report_type if tmpl else ReportType.EXECUTIVE_SUMMARY
        report_format = (fmt or (tmpl.format if tmpl else ReportFormat.PDF)).upper()
        job_title = title or (tmpl.name if tmpl else "Security Report")

        # Mock gathered security metrics snapshot
        data_summary = {
            "total_assets_monitored": 42,
            "critical_vulnerabilities": 3,
            "open_incidents": 2,
            "resolved_incidents": 15,
            "sla_compliance_rate": "98.5%",
            "threat_intel_matches": 8,
            "soar_playbook_executions": 12,
            "mttr_minutes": 14.2
        }
        if parameters:
            data_summary.update(parameters)

        content, file_name, file_size = self.generator.generate_report_content(report_type, report_format, organization_id, data_summary)

        job = ReportJob(
            organization_id=organization_id,
            template_id=template_id,
            title=job_title,
            report_type=report_type,
            format=report_format,
            status=JobStatus.COMPLETED,
            parameters=parameters or {},
            file_name=file_name,
            file_content=content,
            file_size_bytes=file_size,
            generated_by=generated_by
        )
        _REPORT_JOBS_STORE.append(job)

        await self.audit_repo.record_event(
            AuditEvent(
                actor_email=generated_by,
                organization_id=organization_id,
                action="REPORT_GENERATED",
                resource_type="REPORT_JOB",
                resource_id=job.job_id,
                details={"report_type": report_type, "format": report_format, "file_name": file_name}
            )
        )
        return job

    def list_jobs(self, organization_id: str, limit: int = 50) -> List[ReportJob]:
        return [j for j in _REPORT_JOBS_STORE if j.organization_id == organization_id][-limit:]

    def get_job(self, job_id: str) -> Optional[ReportJob]:
        return next((j for j in _REPORT_JOBS_STORE if j.job_id == job_id), None)

    async def export_audit_logs(
        self,
        organization_id: str,
        fmt: str = ReportFormat.CSV,
        requested_by: str = "soc-admin@gestivaone.com"
    ) -> AuditExportRequest:
        events = await self.audit_repo.get_events_by_organization(organization_id)
        events_dicts = [
            {
                "event_id": e.event_id,
                "timestamp": e.timestamp.isoformat(),
                "actor_email": e.actor_email,
                "action": e.action,
                "resource_type": e.resource_type,
                "resource_id": e.resource_id,
                "organization_id": e.organization_id
            } for e in events
        ]

        content, file_name, file_size = self.generator.generate_audit_export(organization_id, fmt.upper(), events_dicts)

        req = AuditExportRequest(
            organization_id=organization_id,
            format=fmt.upper(),
            total_events_exported=len(events),
            status=JobStatus.COMPLETED,
            file_content=content,
            requested_by=requested_by
        )
        _AUDIT_EXPORTS_STORE.append(req)

        await self.audit_repo.record_event(
            AuditEvent(
                actor_email=requested_by,
                organization_id=organization_id,
                action="AUDIT_EXPORT_GENERATED",
                resource_type="AUDIT_EXPORT",
                resource_id=req.export_id,
                details={"format": fmt, "total_events": len(events)}
            )
        )
        return req
