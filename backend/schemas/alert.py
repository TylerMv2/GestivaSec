from pydantic import BaseModel
from datetime import datetime

class AlertBase(BaseModel):
    level: str
    source: str
    description: str
    status: str = "Active"
    notes: str = ""

class AlertResponse(AlertBase):
    id: int
    timestamp: datetime
    host_id: int | None = None
    resolved_at: datetime | None = None

    class Config:
        from_attributes = True

class AlertUpdate(BaseModel):
    status: str
    notes: str | None = None
