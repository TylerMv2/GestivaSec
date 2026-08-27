# Gestiva Security & Observability Plugin Engine - Base Class

class BasePlugin:
    name: str = "BasePlugin"
    description: str = "Base placeholder class for external tool integrations"

    def __init__(self):
        self.enabled = False

    def initialize(self) -> bool:
        """Sets up credentials and connection limits"""
        raise NotImplementedError("Subclasses must override the initialize method.")

    def process_alerts(self, alerts: list) -> bool:
        """Sends alerts payload or ingests security anomalies"""
        raise NotImplementedError("Subclasses must override the process_alerts method.")

    def run_sync(self) -> dict:
        """Syncs indicators of compromise (IoC) or performance profiles"""
        raise NotImplementedError("Subclasses must override the run_sync method.")
