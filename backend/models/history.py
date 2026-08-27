import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.connection import Base

class History(Base):
    __tablename__ = "history"

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("hosts.id", ondelete="CASCADE"), nullable=False)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    metric_name = Column(String, nullable=False, index=True)  # CPU, RAM, Disk, Latency, PacketLoss, NetThroughput
    metric_value = Column(Float, nullable=False)

    # Relationships
    host = relationship("Host", back_populates="history")
