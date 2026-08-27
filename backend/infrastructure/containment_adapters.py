"""
Gestiva Security (GestivaSec V1) — Automated Containment Adapters Infrastructure Component
Executes allowlisted containment actions (MockFirewallAdapter, MockEDRAdapter, MockIdentityAdapter, MockNotificationAdapter).
"""
from typing import Dict, Any, List

_FIREWALL_BLOCKLIST: set = set()
_ISOLATED_ASSETS: set = set()
_DISABLED_USERS: set = set()
_REVOKED_SESSIONS: set = set()
_BLOCKED_DOMAINS: set = set()

class IntegrationAdapter:
    def validate(self, target: str) -> bool:
        return bool(target and isinstance(target, str))

    def execute(self, target: str, dry_run: bool = False) -> Dict[str, Any]:
        raise NotImplementedError

    def verify(self, target: str) -> bool:
        return True

    def rollback(self, target: str) -> Dict[str, Any]:
        raise NotImplementedError

class MockEDRAdapter(IntegrationAdapter):
    def execute(self, target: str, dry_run: bool = False) -> Dict[str, Any]:
        if not dry_run:
            _ISOLATED_ASSETS.add(target)
        return {"action": "ISOLATE_HOST", "asset_id": target, "status": "CONTAINED" if not dry_run else "SIMULATED", "message": f"Asset {target} network interface isolated."}

    def rollback(self, target: str) -> Dict[str, Any]:
        _ISOLATED_ASSETS.discard(target)
        return {"action": "UNISOLATE_HOST", "asset_id": target, "status": "UNCONTAINED", "message": f"Asset {target} isolation removed."}

class MockFirewallAdapter(IntegrationAdapter):
    def execute(self, target: str, dry_run: bool = False) -> Dict[str, Any]:
        if not dry_run:
            _FIREWALL_BLOCKLIST.add(target)
        return {"action": "BLOCK_IP", "target_ip": target, "status": "BLOCKED" if not dry_run else "SIMULATED", "message": f"Perimeter firewall rule applied to {target}."}

    def rollback(self, target: str) -> Dict[str, Any]:
        _FIREWALL_BLOCKLIST.discard(target)
        return {"action": "UNBLOCK_IP", "target_ip": target, "status": "UNBLOCKED", "message": f"Perimeter firewall block rule removed for {target}."}

class MockIdentityAdapter(IntegrationAdapter):
    def execute(self, target: str, dry_run: bool = False) -> Dict[str, Any]:
        if not dry_run:
            _DISABLED_USERS.add(target)
        return {"action": "DISABLE_USER", "user_email": target, "status": "DISABLED" if not dry_run else "SIMULATED", "message": f"User account {target} disabled."}

    def rollback(self, target: str) -> Dict[str, Any]:
        _DISABLED_USERS.discard(target)
        return {"action": "ENABLE_USER", "user_email": target, "status": "ENABLED", "message": f"User account {target} re-enabled."}

class MockNotificationAdapter(IntegrationAdapter):
    def execute(self, target: str, dry_run: bool = False) -> Dict[str, Any]:
        return {"action": "NOTIFY_ANALYST", "recipient": target, "status": "DISPATCHED" if not dry_run else "SIMULATED", "message": f"SOC Notification dispatched to {target}."}

    def rollback(self, target: str) -> Dict[str, Any]:
        return {"action": "NOTIFY_CANCELLED", "recipient": target, "status": "CANCELLED", "message": "Notification record marked cancelled."}


class ContainmentActionAdapters:
    def __init__(self):
        self.edr = MockEDRAdapter()
        self.firewall = MockFirewallAdapter()
        self.identity = MockIdentityAdapter()
        self.notification = MockNotificationAdapter()

    def isolate_asset(self, asset_id: str, dry_run: bool = False) -> Dict[str, Any]:
        res = self.edr.execute(asset_id, dry_run=dry_run)
        res["action"] = "ISOLATE_ASSET"
        return res

    def block_firewall_ip(self, ip_address: str, dry_run: bool = False) -> Dict[str, Any]:
        res = self.firewall.execute(ip_address, dry_run=dry_run)
        res["action"] = "BLOCK_FIREWALL_IP"
        return res

    def dispatch_notification(self, recipient: str, payload: Dict[str, Any], dry_run: bool = False) -> Dict[str, Any]:
        res = self.notification.execute(recipient, dry_run=dry_run)
        res["action"] = "DISPATCH_NOTIFICATION"
        return res

    def get_blocked_ips(self) -> List[str]: return list(_FIREWALL_BLOCKLIST)
    def get_isolated_assets(self) -> List[str]: return list(_ISOLATED_ASSETS)
