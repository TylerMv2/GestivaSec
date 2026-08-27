from sqlalchemy import Column, Integer, String, Boolean, Text
from backend.database.connection import Base

class SettingsModel(Base):
    __tablename__ = "settings"

    id = Column(Integer, primary_key=True, index=True)
    module_name = Column(String, unique=True, index=True, nullable=False)  # PingCollector, HTTPCollector, etc.
    enabled = Column(Boolean, default=True)
    interval_seconds = Column(Integer, default=30)
    configuration = Column(Text, default="{}")  # JSON string configurations specific to the module
