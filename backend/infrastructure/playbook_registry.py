"""
Gestiva Security (GestivaSec V1) — SOAR Playbook Registry Infrastructure Component
Stores active automated response playbooks, trigger rules, and step configurations.
"""
from typing import List, Optional
from datetime import datetime, timezone
from backend.domain.soar_playbook import (
    Playbook,
    PlaybookStep,
    PlaybookAction,
    ActionRiskLevel,
    PlaybookStatus
)

_DEFAULT_PLAYBOOKS = [
    Playbook(
        playbook_id="PB-CONTAIN-HOST",
        organization_id="GLOBAL",
        name="Automated Host Network Isolation",
        title="Automated Host Network Isolation",
        description="Isolates compromised host network interfaces upon P1 Critical finding.",
        trigger_type="P1_CRITICAL_ALERT",
        trigger_event="P1_CRITICAL_ALERT",
        requires_approval=True,
        steps=[
            PlaybookStep(
                step_id="STEP-ISOLATE-01",
                action_type="ISOLATE_HOST",
                adapter_name="MockEDRAdapter",
                target_param="asset_id",
                description="Isolates host network interface.",
                risk_level=ActionRiskLevel.HIGH,
                requires_approval=True
            )
        ],
        actions=[
            PlaybookAction(
                action_type="ISOLATE_ASSET",
                target_param="asset_id",
                description="Sets Asset state to CONTAINED and revokes socket access."
            )
        ]
    ),
    Playbook(
        playbook_id="PB-BLOCK-IP",
        organization_id="GLOBAL",
        name="Automated Perimeter Firewall IP Block",
        title="Automated Perimeter Firewall IP Block",
        description="Pushes malicious IP address to firewall perimeter blocklist.",
        trigger_type="THREAT_INTEL_MATCH",
        trigger_event="THREAT_INTEL_MATCH",
        requires_approval=False,
        steps=[
            PlaybookStep(
                step_id="STEP-BLOCK-IP-01",
                action_type="BLOCK_IP",
                adapter_name="MockFirewallAdapter",
                target_param="target_ip",
                description="Appends malicious IP to perimeter firewall rule.",
                risk_level=ActionRiskLevel.MEDIUM,
                requires_approval=False
            )
        ],
        actions=[
            PlaybookAction(
                action_type="BLOCK_FIREWALL_IP",
                target_param="target_ip",
                description="Appends malicious IP to perimeter iptables/firewall rule."
            )
        ]
    ),
    Playbook(
        playbook_id="PB-NOTIFY-SOC",
        organization_id="GLOBAL",
        name="Dispatch SOC Emergency Notification",
        title="Dispatch SOC Emergency Notification",
        description="Sends high-priority alert dispatch to SOC Tier 2 Analysts.",
        trigger_type="ATTACK_CHAIN",
        trigger_event="ATTACK_CHAIN",
        requires_approval=False,
        steps=[
            PlaybookStep(
                step_id="STEP-NOTIFY-01",
                action_type="NOTIFY_ANALYST",
                adapter_name="MockNotificationAdapter",
                target_param="email",
                description="Formats and sends emergency SOC notification payload.",
                risk_level=ActionRiskLevel.LOW,
                requires_approval=False
            )
        ],
        actions=[
            PlaybookAction(
                action_type="DISPATCH_NOTIFICATION",
                target_param="email",
                description="Formats and sends emergency SOC notification payload."
            )
        ]
    )
]

class PlaybookRegistry:
    def __init__(self):
        self._playbooks: List[Playbook] = list(_DEFAULT_PLAYBOOKS)

    def add_playbook(self, playbook: Playbook) -> Playbook:
        self._playbooks.append(playbook)
        return playbook

    def list_playbooks(self, organization_id: str = "GLOBAL") -> List[Playbook]:
        return [p for p in self._playbooks if p.active and p.organization_id in ["GLOBAL", organization_id]]

    def get_playbook_by_id(self, playbook_id: str) -> Optional[Playbook]:
        for p in self._playbooks:
            if p.playbook_id == playbook_id:
                return p
        return None

    def set_status(self, playbook_id: str, new_status: str) -> Optional[Playbook]:
        pb = self.get_playbook_by_id(playbook_id)
        if pb:
            pb.status = new_status
            pb.active = (new_status == PlaybookStatus.ACTIVE)
            pb.updated_at = datetime.now(timezone.utc)
        return pb
