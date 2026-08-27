"""
Gestiva Security (GestivaSec V1) — Detection Rules Registry Infrastructure Component
Stores and manages detection rule definitions in memory with MITRE ATT&CK mapping.
"""
from typing import List, Optional
from backend.domain.detection_rule import DetectionRule, DetectionRuleCondition

_DEFAULT_RULES = [
    DetectionRule(
        rule_id="RULE-BRUTE-FORCE-01",
        title="SSH / Auth Brute Force Attempt Detected",
        description="Triggers when a login failure action occurs on an authentication source.",
        severity="P1_CRITICAL",
        category="AUTHENTICATION",
        mitre_attack_id="T1110.001",
        condition=DetectionRuleCondition(
            field_path="event.action",
            operator="EQUALS",
            target_value="LOGIN_FAILED",
            threshold_count=1,
            time_window_seconds=60
        )
    ),
    DetectionRule(
        rule_id="RULE-WIN-PRIV-ESCALATION",
        title="Windows Privilege Escalation Attack Detected",
        description="Triggers on EVTX EventID 4672 privilege escalation events.",
        severity="P1_CRITICAL",
        category="AUTHENTICATION",
        mitre_attack_id="T1068",
        condition=DetectionRuleCondition(
            field_path="event.action",
            operator="EQUALS",
            target_value="PRIVILEGE_ESCALATION",
            threshold_count=1,
            time_window_seconds=60
        )
    ),
    DetectionRule(
        rule_id="RULE-EXTERNAL-GEOIP-ANOMALY",
        title="Anomalous External GeoIP Connection",
        description="Triggers on external non-internal GeoIP source events.",
        severity="P2_HIGH",
        category="NETWORK",
        mitre_attack_id="T1071",
        condition=DetectionRuleCondition(
            field_path="source.geo_country",
            operator="EQUALS",
            target_value="US",
            threshold_count=1,
            time_window_seconds=60
        )
    )
]

class RulesRegistry:
    def __init__(self):
        self._rules = list(_DEFAULT_RULES)

    def list_rules(self, include_inactive: bool = False) -> List[DetectionRule]:
        """Returns active detection rules or all rules."""
        if include_inactive:
            return list(self._rules)
        return [r for r in self._rules if r.active]

    def add_rule(self, rule: DetectionRule) -> DetectionRule:
        """Registers a new detection rule."""
        self._rules.append(rule)
        return rule

    def get_rule_by_id(self, rule_id: str) -> Optional[DetectionRule]:
        for r in self._rules:
            if r.rule_id == rule_id:
                return r
        return None

    def update_rule(self, rule_id: str, title: Optional[str] = None, description: Optional[str] = None, severity: Optional[str] = None, active: Optional[bool] = None) -> Optional[DetectionRule]:
        rule = self.get_rule_by_id(rule_id)
        if not rule:
            return None
        if title is not None: rule.title = title
        if description is not None: rule.description = description
        if severity is not None: rule.severity = severity
        if active is not None: rule.active = active
        return rule

    def enable_rule(self, rule_id: str) -> Optional[DetectionRule]:
        return self.update_rule(rule_id, active=True)

    def disable_rule(self, rule_id: str) -> Optional[DetectionRule]:
        return self.update_rule(rule_id, active=False)

