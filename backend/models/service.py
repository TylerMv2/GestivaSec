import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.connection import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    host_id = Column(Integer, ForeignKey("hosts.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, index=True, nullable=False)  # HTTP, HTTPS, SSH, DNS, SMB, etc.
    port = Column(Integer, nullable=False)
    status = Column(String, default="DOWN")  # UP, DOWN
    response_time_ms = Column(Float, default=0.0)
    version = Column(String, default="Unknown")
    last_check = Column(DateTime, default=datetime.datetime.utcnow)
    metadata_json = Column(Text, default="{}")  # Extra metadata, JSON string

    # Relationships
    host = relationship("Host", back_populates="services")
    certificates = relationship("Certificate", back_populates="service", cascade="all, delete-orphan")
