"""
Gestiva Security (GestivaSec V1) — Distributed Continuous Monitoring REST API Router
Exposes /api/v1/soc/scheduler endpoints for 1m (HTTP), 5m (DNS), 1h (TLS) jobs and Change Audit Trail.
"""
from typing import List, Dict, Optional
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from backend.application.soc_scheduler_service import SOCSchedulerService

router = APIRouter(prefix="/api/v1/soc/scheduler", tags=["SOC Continuous Monitoring Scheduler"])
scheduler_service = SOCSchedulerService()

class JobSchema(BaseModel):
    job_id: str
    target_asset_id: str
    target_url: str
    interval: str
    job_type: str
    last_run_at: Optional[str]
    status: str

class ChangeLogSchema(BaseModel):
    target_url: str
    change_category: str
    property_name: str
    old_value: str
    new_value: str
    detected_at: str

@router.get("/jobs", response_model=List[JobSchema])
async def list_jobs():
    """Lists all configured 1m, 5m, and 1h distributed SOC observation jobs."""
    jobs = await scheduler_service.list_scheduled_jobs()
    return [
        JobSchema(
            job_id=j.job_id,
            target_asset_id=j.target_asset_id,
            target_url=j.target_url,
            interval=j.interval.value,
            job_type=j.job_type,
            last_run_at=j.last_run_at.isoformat() if j.last_run_at else None,
            status=j.status
        )
        for j in jobs
    ]

@router.post("/trigger/{job_id}", status_code=status.HTTP_200_OK)
async def trigger_job(job_id: str):
    """Manually triggers immediate execution of a scheduled 1m, 5m, or 1h SOC job."""
    try:
        details = await scheduler_service._engine.execute_job(job_id)
        return {"job_id": job_id, "status": "SUCCESS", "details": details}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/changes", response_model=List[ChangeLogSchema])
async def get_detected_changes():
    """Retrieves audit trail of all infrastructure and security state changes."""
    changes = scheduler_service._engine.get_change_store()
    return [
        ChangeLogSchema(
            target_url=c.target_url,
            change_category=c.change_category,
            property_name=c.property_name,
            old_value=c.old_value,
            new_value=c.new_value,
            detected_at=c.detected_at.isoformat()
        )
        for c in changes
    ]
