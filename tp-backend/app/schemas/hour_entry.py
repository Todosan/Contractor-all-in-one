from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ----- HourEntry schemas -----
class HourEntryBase(BaseModel):
    task_id: Optional[int] = None
    date: datetime
    hours: float
    notes: Optional[str] = None

class HourEntryCreate(HourEntryBase):
    """Schema for creating a new HourEntry"""
    pass

class HourEntryUpdate(BaseModel):
    task_id: Optional[int]
    date: Optional[datetime]
    hours: Optional[float]
    notes: Optional[str]

class HourEntryRead(HourEntryBase):
    id: int

    class Config:
        orm_mode = True