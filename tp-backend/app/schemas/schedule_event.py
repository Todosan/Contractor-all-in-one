from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ----- ScheduleEvent schemas -----
class ScheduleEventBase(BaseModel):
    title: str
    description: Optional[str] = None
    start: datetime
    end: datetime

class ScheduleEventCreate(ScheduleEventBase):
    """Schema for creating a new ScheduleEvent"""
    pass

class ScheduleEventUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    start: Optional[datetime]
    end: Optional[datetime]

class ScheduleEventRead(ScheduleEventBase):
    id: int

    class Config:
        orm_mode = True