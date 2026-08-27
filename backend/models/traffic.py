import datetime
from sqlalchemy import Column, Integer, String, Float, Text, DateTime
from backend.database.connection import Base

class Traffic(Base):
    __tablename__ = "traffic"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow, index=True)
    protocol = Column(String, nullable=False, index=True)  # HTTP, HTTPS, DNS, SSH, SMB, ICMP, NTP, RDP, etc.
    port = Column(Integer, nullable=False, index=True)
    source_ip = Column(String, nullable=False, index=True)
    dest_ip = Column(String, nullable=False, index=True)
    source_port = Column(Integer, nullable=False)
    dest_port = Column(Integer, nullable=False)
    volume_bytes = Column(Integer, default=0)
    latency_ms = Column(Float, default=0.0)
    connection_state = Column(String, default="CLOSED")  # ESTABLISHED, CLOSED, LISTEN, etc.
    metadata_json = Column(Text, default="{}")  # JSON string metadata (e.g. SNI, DNS queries, TLS version)
