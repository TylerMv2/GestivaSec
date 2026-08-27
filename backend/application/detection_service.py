"""
Gestiva Security (GestivaSec V1) — SPRINT 6: Detection & Alerts Application Service
Evaluates Normalized Events (GES) against Rules, generates Findings, and promotes/deduplicates Alerts.
"""
import re
from datetime import datetime, timezone
from typing import List, Dict, Any, Optional
from backend.domain.normalized_event import NormalizedEvent
from backend.domain.detection_rule import DetectionRule, Finding, ActionableAlert
from backend.infrastructure.rules_registry import RulesRegistry

_FINDINGS_STORE: List[Finding] = []
_ALERTS_STORE: List[ActionableAlert] = []

class DetectionEngineService:
    def __init__(self, registry: Optional[RulesRegistry] = None):
        self.registry = registry or RulesRegistry()

    def _extract_field_value(self, event: NormalizedEvent, field_path: str) -> Any:
        """Extracts field value dynamically from NormalizedEvent (GES)."""
        parts = field_path.split(".")
        val = event
        for p in parts:
            if hasattr(val, p):
                val = getattr(val, p)
            elif isinstance(val, dict) and p in val:
                val = val[p]
            else:
                return None
        return val

    def _evaluate_rule(self, rule: DetectionRule, event: NormalizedEvent) -> bool:
        """Evaluates rule condition against NormalizedEvent (GES)."""
        cond = rule.condition
        actual_val = self._extract_field_value(event, cond.field_path)
        if actual_val is None:
            return False

        op = cond.operator.upper()
        target = cond.target_value

        if op == "EQUALS":
            return str(actual_val) == str(target)
        elif op == "CONTAINS":
            return str(target).lower() in str(actual_val).lower()
        elif op == "REGEX":
            return bool(re.search(str(target), str(actual_val)))
        
        return False

    async def process_normalized_event(self, event: NormalizedEvent) -> List[Finding]:
        """Evaluates normalized event against all active rules and promotes findings to alerts."""
        active_rules = self.registry.list_rules()
        generated_findings = []

        for rule in active_rules:
            if self._evaluate_rule(rule, event):
                # 1. Create Finding
                finding = Finding(
                    organization_id=event.organization_id,
                    rule_id=rule.rule_id,
                    rule_title=rule.title,
                    severity=rule.severity,
                    asset_id=event.destination.asset_id,
                    source_ip=event.source.ip,
                    matched_event_ids=[event.event_id],
                    confidence_score=0.95
                )
                _FINDINGS_STORE.append(finding)
                generated_findings.append(finding)

                # 2. Promote & Deduplicate Alert
                await self._promote_or_deduplicate_alert(finding, rule)

                # 3. Trigger Correlation Engine (Sprint 7)
                try:
                    from backend.application.correlation_service import CorrelationEngineService
                    correlator = CorrelationEngineService()
                    await correlator.process_finding(finding)
                except Exception:
                    pass

        return generated_findings

    async def _promote_or_deduplicate_alert(self, finding: Finding, rule: DetectionRule) -> ActionableAlert:
        """Deduplicates alert if existing alert matches Asset UUID + Rule ID in active state."""
        now = datetime.now(timezone.utc)
        
        # Check for existing alert with same rule and asset/source_ip in non-closed status
        for alert in _ALERTS_STORE:
            if (alert.organization_id == finding.organization_id and
                alert.rule_id == finding.rule_id and
                alert.asset_id == finding.asset_id and
                alert.status in ["NEW", "IN_PROGRESS"]):
                
                # Deduplicate & Increment
                alert.findings_count += 1
                alert.last_seen = now
                return alert

        # Create new ActionableAlert
        new_alert = ActionableAlert(
            organization_id=finding.organization_id,
            rule_id=rule.rule_id,
            title=rule.title,
            severity=rule.severity,
            asset_id=finding.asset_id,
            source_ip=finding.source_ip,
            status="NEW",
            mitre_attack_id=rule.mitre_attack_id,
            findings_count=1,
            first_seen=now,
            last_seen=now
        )
        _ALERTS_STORE.append(new_alert)
        return new_alert

    def get_finding(self, finding_id: str) -> Optional[Finding]:
        for f in _FINDINGS_STORE:
            if f.finding_id == finding_id:
                return f
        return None

    def list_findings(self, organization_id: str, limit: int = 50) -> List[Finding]:
        """Returns findings for tenant (BR-0004)."""
        filtered = [f for f in _FINDINGS_STORE if f.organization_id == organization_id]
        return filtered[-limit:]

    def get_alert(self, alert_id: str) -> Optional[ActionableAlert]:
        for a in _ALERTS_STORE:
            if a.alert_id == alert_id:
                return a
        return None

    def list_alerts(self, organization_id: str, limit: int = 50) -> List[ActionableAlert]:
        """Returns actionable alerts for tenant (BR-0004)."""
        filtered = [a for a in _ALERTS_STORE if a.organization_id == organization_id]
        return filtered[-limit:]

    def update_alert_status(self, alert_id: str, new_status: str) -> Optional[ActionableAlert]:
        """Updates alert status (NEW -> ACKNOWLEDGED -> IN_PROGRESS -> SUPPRESSED -> CLOSED -> DISMISSED)."""
        valid_statuses = ["NEW", "ACKNOWLEDGED", "IN_PROGRESS", "CONTAINED", "SUPPRESSED", "CLOSED", "DISMISSED"]
        if new_status.upper() not in valid_statuses:
            return None

        for alert in _ALERTS_STORE:
            if alert.alert_id == alert_id:
                alert.status = new_status.upper()
                return alert
        return None

