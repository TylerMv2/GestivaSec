"""
Gestiva Security (GestivaSec V1) — SOC Scheduler Application Service
"""
from typing import List
from backend.domain.soc_scheduler import SOCScheduleJob, JobExecutionLog
from backend.infrastructure.soc_scheduler_engine import SOCSchedulerEngine

class SOCSchedulerService:
    _engine = SOCSchedulerEngine()

    async def list_scheduled_jobs(self) -> List[SOCScheduleJob]:
        return self._engine.list_jobs()

    async def trigger_job_manually(self, job_id: str) -> JobExecutionLog:
        return await self._engine.execute_job(job_id)

    async def get_execution_history(self) -> List[JobExecutionLog]:
        return self._engine.get_history()
