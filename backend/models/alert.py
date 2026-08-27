import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from backend.database.connection import Base

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    level = Column(String, nullable=False, index=True)  # Info, Warning, Important, Critical
    source = Column(String, nullable=False, index=True)  # host / service name
    host_id = Column(Integer, ForeignKey("hosts.id", ondelete="CASCADE"), nullable=True)
    description = Column(Text, nullable=False)
    status = Column(String, default="Active", index=True)  # Active, Acknowledged, Resolved
    resolved_at = Column(DateTime, nullable=True)
    notes = Column(Text, default="")
