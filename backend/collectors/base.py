import logging
import datetime
import traceback
from backend.database.connection import SessionLocal
from backend.models.settings import SettingsModel
from backend.models.log import Log
from backend.models.alert import Alert
from backend.models.history import History
from backend.models.event import Event

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("CollectorBase")

class BaseCollector:
    name: str = "BaseCollector"

    def __init__(self):
        self.db = SessionLocal()
        self.config = self._load_config()

    def _load_config(self) -> dict:
        """Loads collector configuration from settings table"""
        try:
            settings_rec = self.db.query(SettingsModel).filter(SettingsModel.module_name == self.name).first()
            if settings_rec:
                import json
                return {
                    "enabled": settings_rec.enabled,
                    "interval": settings_rec.interval_seconds,
                    **json.loads(settings_rec.configuration)
                }
        except Exception as e:
            logger.error(f"Failed to load configuration for {self.name}: {e}")
        return {"enabled": True, "interval": 30}

    def is_enabled(self) -> bool:
        self.config = self._load_config()
        return self.config.get("enabled", True)

    def log_message(self, host_id: int, ip: str, message: str, level: str = "Info", service: str = None) -> Log:
        """Logs a message directly to the database for this host"""
        service_name = service if service else self.name
        log_entry = Log(
            host_id=host_id,
            source_ip=ip,
            level=level,
            service=service_name,
            message=message,
            timestamp=datetime.datetime.utcnow()
        )
        self.db.add(log_entry)
        self.db.commit()
        return log_entry

    def raise_alert(self, host_id: int, level: str, source: str, description: str) -> Alert:
        """Raises a new alert if it does not already exist as active"""
        # Check if the source service category has alerting suppressed in settings
        try:
            from backend.models.settings import SettingsModel
            import json
            
            integrations = self.db.query(SettingsModel).filter(SettingsModel.module_name == "API_Integrations").first()
            if integrations and integrations.configuration:
                config_dict = json.loads(integrations.configuration)
                suppressed = config_dict.get("suppressed_alert_categories", [])
                if source in suppressed:
                    # Logging local event that alerting is suppressed
                    self.log_message(
                        host_id=host_id,
                        ip="127.0.0.1",
                        message=f"Alert for {source} suppressed by configuration policy: {description}",
                        level="Info",
                        service="System"
                    )
                    return None
        except Exception as e:
            # Fallback in case of database table or parsing errors
            pass

        # Avoid duplicate active alerts for the same source/description
        existing = self.db.query(Alert).filter(
            Alert.host_id == host_id,
            Alert.source == source,
            Alert.status == "Active",
            Alert.description == description
        ).first()
        
        if existing:
            return existing

        alert = Alert(
            timestamp=datetime.datetime.utcnow(),
            level=level,
            source=source,
            host_id=host_id,
            description=description,
            status="Active"
        )
        self.db.add(alert)
        self.db.commit()
        
        # Log event for audit trail
        self.log_event("Security", f"Alert raised for {source}: {description}", {"level": level})
        return alert

    def resolve_alerts(self, host_id: int, source: str):
        """Resolves active alerts for a source when conditions return to normal"""
        active_alerts = self.db.query(Alert).filter(
            Alert.host_id == host_id,
            Alert.source == source,
            Alert.status == "Active"
        ).all()
        for alert in active_alerts:
            alert.status = "Resolved"
            alert.resolved_at = datetime.datetime.utcnow()
        if active_alerts:
            self.db.commit()

    def save_metric(self, host_id: int, metric_name: str, value: float) -> History:
        """Saves a metric history snapshot"""
        history_entry = History(
            host_id=host_id,
            timestamp=datetime.datetime.utcnow(),
            metric_name=metric_name,
            metric_value=value
        )
        self.db.add(history_entry)
        self.db.commit()
        return history_entry

    def log_event(self, event_type: str, message: str, details: dict = None) -> Event:
        """Log general platform events"""
        import json
        evt = Event(
            timestamp=datetime.datetime.utcnow(),
            type=event_type,
            source=self.name,
            message=message,
            details=json.dumps(details or {})
        )
        self.db.add(evt)
        self.db.commit()
        return evt

    def run(self):
        """Main execution function to be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement the run method")

    def close(self):
        self.db.close()
