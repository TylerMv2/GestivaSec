import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.connection import Base

class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    host_id = Column(Integer, ForeignKey("hosts.id", ondelete="CASCADE"), nullable=False)
    source_ip = Column(String, nullable=False, index=True)
    level = Column(String, default="Info", index=True)  # Info, Warn, Error, Debug
    service = Column(String, default="system", index=True)
    message = Column(Text, nullable=False)
    raw_log = Column(Text, default="")

    # Relationships
    host = relationship("Host", back_populates="logs")
