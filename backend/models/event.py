import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from backend.database.connection import Base

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    type = Column(String, nullable=False, index=True)  # System, Audit, Security
    source = Column(String, nullable=False, index=True)  # Core engine, API, Webhook
    message = Column(Text, nullable=False)
    details = Column(Text, default="{}")  # JSON string
