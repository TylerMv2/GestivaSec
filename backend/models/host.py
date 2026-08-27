import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from sqlalchemy.orm import relationship
from backend.database.connection import Base

class Host(Base):
    __tablename__ = "hosts"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, index=True, nullable=False)
    ip = Column(String, index=True, nullable=False)
    os = Column(String, default="Unknown")
    status = Column(String, default="UNKNOWN")  # UP, DOWN, UNKNOWN
    latency_ms = Column(Float, default=0.0)
    ports_authorized = Column(Text, default="[]")  # JSON string list of integers
    classification = Column(String, default="Server")  # Firewall, Switch, Server, VM, etc.
    notes = Column(Text, default="")
    tags = Column(Text, default="[]")  # JSON string list of tags
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    services = relationship("Service", back_populates="host", cascade="all, delete-orphan")
    logs = relationship("Log", back_populates="host", cascade="all, delete-orphan")
    inventory = relationship("Inventory", back_populates="host", cascade="all, delete-orphan")
    certificates = relationship("Certificate", back_populates="host", cascade="all, delete-orphan")
    history = relationship("History", back_populates="host", cascade="all, delete-orphan")
