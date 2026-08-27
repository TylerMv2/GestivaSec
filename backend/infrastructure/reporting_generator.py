"""
Gestiva Security (GestivaSec V1) — STAGE 11: Report & Audit Export Generator Infrastructure Component
Generates structured PDF/CSV/JSON executive reports and compliance audit exports for SOC operations.
"""
import csv
import json
import io
from typing import Dict, Any, List
from datetime import datetime, timezone
from backend.domain.reporting import ReportType, ReportFormat, ReportJob, AuditExportRequest

class ReportingGenerator:
    def generate_report_content(
        self,
        report_type: str,
        fmt: str,
        organization_id: str,
        data_summary: Dict[str, Any]
    ) -> tuple[str, str, int]:
        """Generates report content string, file_name, and file_size_bytes."""
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        ext = fmt.lower()
        file_name = f"GestivaSec_{report_type}_{organization_id[:8]}_{timestamp_str}.{ext}"

        if fmt == ReportFormat.JSON:
            content = json.dumps({
                "platform": "GestivaSec V1 Enterprise SOC Platform",
                "organization_id": organization_id,
                "report_type": report_type,
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "summary": data_summary
            }, indent=2)

        elif fmt == ReportFormat.CSV:
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["Metric / Category", "Value", "Notes"])
            for k, v in data_summary.items():
                writer.writerow([k, str(v), f"Tenant {organization_id[:8]} snapshot"])
            content = output.getvalue()

        else: # PDF / Text representation
            lines = [
                "================================================================================",
                "GESTIVA SECURITY ENTERPRISE SOC PLATFORM — EXECUTIVE REPORT",
                "================================================================================",
                f"Organization ID : {organization_id}",
                f"Report Type     : {report_type}",
                f"Generated At    : {datetime.now(timezone.utc).isoformat()}",
                "--------------------------------------------------------------------------------",
                "EXECUTIVE SUMMARY & SECURITY METRICS:",
            ]
            for k, v in data_summary.items():
                lines.append(f"  • {k.replace('_', ' ').title():<30} : {v}")
            lines.append("================================================================================")
            content = "\n".join(lines)

        file_size = len(content.encode("utf-8"))
        return content, file_name, file_size

    def generate_audit_export(
        self,
        organization_id: str,
        fmt: str,
        audit_events: List[Dict[str, Any]]
    ) -> tuple[str, str, int]:
        """Generates audit log export payload in CSV or JSON format."""
        timestamp_str = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        ext = fmt.lower()
        file_name = f"GestivaSec_Audit_Export_{organization_id[:8]}_{timestamp_str}.{ext}"

        if fmt == ReportFormat.JSON:
            content = json.dumps({
                "organization_id": organization_id,
                "total_events": len(audit_events),
                "exported_at": datetime.now(timezone.utc).isoformat(),
                "audit_events": audit_events
            }, indent=2)
        else:
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(["event_id", "timestamp", "actor_email", "action", "resource_type", "resource_id", "organization_id"])
            for evt in audit_events:
                writer.writerow([
                    evt.get("event_id", ""),
                    evt.get("timestamp", ""),
                    evt.get("actor_email", ""),
                    evt.get("action", ""),
                    evt.get("resource_type", ""),
                    evt.get("resource_id", ""),
                    evt.get("organization_id", "")
                ])
            content = output.getvalue()

        file_size = len(content.encode("utf-8"))
        return content, file_name, file_size
