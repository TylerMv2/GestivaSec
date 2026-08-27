"""
Gestiva Security (GestivaSec V1) — STAGE 11: Enterprise Reporting REST API Router
Exposes REST endpoints for Report Templates, Generation Jobs, Downloads, and Audit Export.
"""
from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException, Header, Response
from pydantic import BaseModel, Field

from backend.application.reporting_service import ReportingApplicationService

router = APIRouter(prefix="/api/v1/reports", tags=["Enterprise Reporting & Audit Export Engine"])
reporting_service = ReportingApplicationService()

# --- REQUEST / DTO MODELS ---
class GenerateReportRequest(BaseModel):
    template_id: str = Field("TMPL-EXEC-01", json_schema_extra={"example": "TMPL-EXEC-01"})
    title: Optional[str] = Field(None, json_schema_extra={"example": "Q3 Executive Security Summary"})
    format: Optional[str] = Field("PDF", json_schema_extra={"example": "PDF"})
    parameters: Optional[Dict[str, Any]] = None

class AuditExportApiRequest(BaseModel):
    format: str = Field("CSV", json_schema_extra={"example": "CSV"})

class ReportTemplateDTO(BaseModel):
    template_id: str
    name: str
    report_type: str
    format: str
    description: str
    sections: List[str]

class ReportJobDTO(BaseModel):
    job_id: str
    organization_id: str
    template_id: str
    title: str
    report_type: str
    format: str
    status: str
    file_name: str
    file_size_bytes: int
    generated_by: str
    generated_at: str

class AuditExportDTO(BaseModel):
    export_id: str
    organization_id: str
    format: str
    total_events_exported: int
    status: str
    requested_by: str
    requested_at: str


# --- REPORT ENDPOINTS ---
@router.get("/templates", response_model=List[ReportTemplateDTO])
async def list_report_templates():
    """Lists available report templates."""
    templates = reporting_service.list_templates()
    return [
        ReportTemplateDTO(
            template_id=t.template_id,
            name=t.name,
            report_type=t.report_type,
            format=t.format,
            description=t.description,
            sections=t.sections
        ) for t in templates
    ]

@router.get("/templates/{template_id}", response_model=ReportTemplateDTO)
async def get_report_template(template_id: str):
    """Retrieves single report template details."""
    t = reporting_service.get_template(template_id)
    if not t:
        raise HTTPException(status_code=404, detail="Report template not found.")
    return ReportTemplateDTO(
        template_id=t.template_id,
        name=t.name,
        report_type=t.report_type,
        format=t.format,
        description=t.description,
        sections=t.sections
    )

@router.post("/generate", response_model=ReportJobDTO, status_code=201)
async def generate_report(req: GenerateReportRequest, x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Generates an executive, technical, or compliance security report."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    job = await reporting_service.generate_report(
        organization_id=org_id,
        template_id=req.template_id,
        title=req.title,
        fmt=req.format,
        parameters=req.parameters
    )
    return ReportJobDTO(
        job_id=job.job_id,
        organization_id=job.organization_id,
        template_id=job.template_id,
        title=job.title,
        report_type=job.report_type,
        format=job.format,
        status=job.status,
        file_name=job.file_name,
        file_size_bytes=job.file_size_bytes,
        generated_by=job.generated_by,
        generated_at=job.generated_at.isoformat()
    )

@router.get("/jobs", response_model=List[ReportJobDTO])
async def list_report_jobs(x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Lists generated report jobs for tenant."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    jobs = reporting_service.list_jobs(org_id)
    return [
        ReportJobDTO(
            job_id=j.job_id,
            organization_id=j.organization_id,
            template_id=j.template_id,
            title=j.title,
            report_type=j.report_type,
            format=j.format,
            status=j.status,
            file_name=j.file_name,
            file_size_bytes=j.file_size_bytes,
            generated_by=j.generated_by,
            generated_at=j.generated_at.isoformat()
        ) for j in jobs
    ]

@router.get("/jobs/{job_id}", response_model=ReportJobDTO)
async def get_report_job(job_id: str):
    """Retrieves metadata of a report generation job."""
    job = reporting_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Report job not found.")
    return ReportJobDTO(
        job_id=job.job_id,
        organization_id=job.organization_id,
        template_id=job.template_id,
        title=job.title,
        report_type=job.report_type,
        format=job.format,
        status=job.status,
        file_name=job.file_name,
        file_size_bytes=job.file_size_bytes,
        generated_by=job.generated_by,
        generated_at=job.generated_at.isoformat()
    )

@router.get("/jobs/{job_id}/download")
async def download_report(job_id: str):
    """Downloads report content (PDF text, CSV, or JSON)."""
    job = reporting_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Report job not found.")

    media_type = "application/json" if job.format == "JSON" else ("text/csv" if job.format == "CSV" else "text/plain")
    return Response(
        content=job.file_content,
        media_type=media_type,
        headers={"Content-Disposition": f"attachment; filename={job.file_name}"}
    )

@router.post("/audit/export", response_model=AuditExportDTO, status_code=201)
async def export_audit_logs(req: AuditExportApiRequest, x_organization_id: Optional[str] = Header(None, alias="X-Organization-ID")):
    """Exports system audit logs for compliance auditing."""
    org_id = x_organization_id or "00000000-0000-0000-0000-000000000001"
    audit_exp = await reporting_service.export_audit_logs(organization_id=org_id, fmt=req.format)
    return AuditExportDTO(
        export_id=audit_exp.export_id,
        organization_id=audit_exp.organization_id,
        format=audit_exp.format,
        total_events_exported=audit_exp.total_events_exported,
        status=audit_exp.status,
        requested_by=audit_exp.requested_by,
        requested_at=audit_exp.requested_at.isoformat()
    )
