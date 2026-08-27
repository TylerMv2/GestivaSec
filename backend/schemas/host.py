from pydantic import BaseModel
from datetime import datetime

class HostBase(BaseModel):
    hostname: str
    ip: str
    os: str = "Unknown"
    classification: str = "Server"
    ports_authorized: str = "[]"
    notes: str = ""
    tags: str = "[]"

class HostCreate(HostBase):
    pass

class HostUpdate(BaseModel):
    hostname: str | None = None
    ip: str | None = None
    os: str | None = None
    classification: str | None = None
    ports_authorized: str | None = None
    notes: str | None = None
    tags: str | None = None
    status: str | None = None

class HostResponse(HostBase):
    id: int
    status: str
    latency_ms: float
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
