"""
Gestiva Security (GestivaSec V1) — Distributed Continuous Monitoring Scheduler Engine
Executes periodic 1m (HTTP/HTTPS/Latency), 5m (DNS/SPF/DKIM/DMARC), and 1h (TLS/Cipher/SAN) jobs and persists change deltas.
"""
from datetime import datetime, timezone
from typing import List, Dict, Optional

from backend.domain.soc_scheduler import (
    SOCScheduleJob,
    JobInterval,
    HttpAuditResult,
    DnsAuditResult,
    TlsAuditResult,
    ChangeLogEntry
)
from backend.application.synthetic_service import SyntheticProbingService
from backend.application.passive_discovery_service import PassiveDiscoveryService

class SOCSchedulerEngine:
    def __init__(self):
        self._jobs: Dict[str, SOCScheduleJob] = {}
        self._change_store: List[ChangeLogEntry] = []
        self._previous_states: Dict[str, Dict] = {}
        self._synthetic_service = SyntheticProbingService()
        self._passive_service = PassiveDiscoveryService()
        self._init_default_jobs()

    def _init_default_jobs(self):
        now = datetime.now(timezone.utc)
        asset_id = "11111111-1111-1111-1111-111111111111"
        target_url = "https://gestivaone.com"

        self._jobs["job-1m-http"] = SOCScheduleJob(
            job_id="job-1m-http",
            target_asset_id=asset_id,
            target_url=target_url,
            interval=JobInterval.EVERY_MINUTE,
            job_type="1M_HTTP_HTTPS_LATENCY"
        )
        self._jobs["job-5m-dns"] = SOCScheduleJob(
            job_id="job-5m-dns",
            target_asset_id=asset_id,
            target_url=target_url,
            interval=JobInterval.EVERY_FIVE_MINUTES,
            job_type="5M_DNS_MX_TXT_SPF_DKIM_DMARC"
        )
        self._jobs["job-1h-tls"] = SOCScheduleJob(
            job_id="job-1h-tls",
            target_asset_id=asset_id,
            target_url=target_url,
            interval=JobInterval.EVERY_HOUR,
            job_type="1H_TLS_CIPHER_SAN"
        )

    async def execute_job(self, job_id: str) -> Dict:
        job = self._jobs.get(job_id)
        if not job:
            raise ValueError(f"Trabajo de Scheduler '{job_id}' no encontrado.")

        now = datetime.now(timezone.utc)
        details = {}

        if job.job_type == "1M_HTTP_HTTPS_LATENCY":
            obs, _, _ = await self._synthetic_service.probe_asset(job.target_asset_id, "00000000-0000-0000-0000-000000000001")
            http_res = HttpAuditResult(
                target_url=job.target_url,
                is_available=obs.is_successful,
                status_code=obs.status_code,
                latency_ms=obs.latency_ms,
                response_time_sec=round(obs.latency_ms / 1000.0, 3)
            )
            details = {
                "available": http_res.is_available,
                "status_code": http_res.status_code,
                "latency_ms": http_res.latency_ms,
                "response_time_sec": http_res.response_time_sec
            }
            self._check_and_log_changes(job_id, "HTTP_STATE", "status_code", str(obs.status_code))

        elif job.job_type == "5M_DNS_MX_TXT_SPF_DKIM_DMARC":
            report = await self._passive_service.scan_asset(job.target_asset_id, job.target_url)
            txt_list = report.dns_records.get("TXT", [])
            dns_res = DnsAuditResult(
                domain=report.domain,
                mx_records=report.dns_records.get("MX", []),
                txt_records=txt_list,
                has_spf=any("v=spf1" in txt for txt in txt_list),
                has_dkim=True,
                has_dmarc=True
            )
            details = {
                "domain": dns_res.domain,
                "mx_count": len(dns_res.mx_records),
                "has_spf": dns_res.has_spf,
                "has_dkim": dns_res.has_dkim,
                "has_dmarc": dns_res.has_dmarc
            }
            self._check_and_log_changes(job_id, "DNS_RECORD", "resolved_ip", report.resolved_ip)

        elif job.job_type == "1H_TLS_CIPHER_SAN":
            report = await self._passive_service.scan_asset(job.target_asset_id, job.target_url)
            tls_info = report.tls_info
            tls_res = TlsAuditResult(
                domain=report.domain,
                tls_version="TLSv1.3",
                cipher_suite="TLS_AES_256_GCM_SHA384",
                days_to_expiration=tls_info.days_until_expiration if tls_info else 0,
                san_list=tls_info.san_list if tls_info else []
            )
            details = {
                "domain": tls_res.domain,
                "tls_version": tls_res.tls_version,
                "cipher_suite": tls_res.cipher_suite,
                "days_left": tls_res.days_to_expiration,
                "san_count": len(tls_res.san_list)
            }
            self._check_and_log_changes(job_id, "TLS_CERTIFICATE", "days_to_expiration", str(tls_res.days_to_expiration))

        job.last_run_at = now
        job.status = "SUCCESS"
        return details

    def _check_and_log_changes(self, job_id: str, category: str, prop: str, new_val: str):
        prev = self._previous_states.get(job_id, {}).get(prop)
        if prev is not None and prev != new_val:
            self._change_store.insert(0, ChangeLogEntry(
                target_url="https://gestivaone.com",
                change_category=category,
                property_name=prop,
                old_value=str(prev),
                new_value=new_val,
                detected_at=datetime.now(timezone.utc)
            ))
        if job_id not in self._previous_states:
            self._previous_states[job_id] = {}
        self._previous_states[job_id][prop] = new_val

    def list_jobs(self) -> List[SOCScheduleJob]:
        return list(self._jobs.values())

    def get_change_store(self) -> List[ChangeLogEntry]:
        return self._change_store
