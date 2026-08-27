import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from backend.database.connection import Base

class Certificate(Base):
    __tablename__ = "certificates"

    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey("services.id", ondelete="CASCADE"), nullable=False)
    host_id = Column(Integer, ForeignKey("hosts.id", ondelete="CASCADE"), nullable=False)
    domain = Column(String, index=True, nullable=False)
    issuer = Column(String, default="Unknown")
    signature_algorithm = Column(String, default="Unknown")
    valid_from = Column(DateTime)
    valid_to = Column(DateTime)
    days_remaining = Column(Integer, default=0)
    status = Column(String, default="Valid")  # Valid, Expiring, Expired
    cipher_suite = Column(String, default="Unknown")
    tls_version = Column(String, default="Unknown")
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationships
    host = relationship("Host", back_populates="certificates")
    service = relationship("Service", back_populates="certificates")
