from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from app.schemas.task import TaskRead

# ----- Invoice schemas -----
class InvoiceBase(BaseModel):
    invoice_number: str
    client_name: str
    description: str
    amount: float
    issued_at: Optional[datetime] = None
    due_date: datetime
    paid: bool = False

class InvoiceCreate(InvoiceBase):
    """Schema for creating a new Invoice"""
    task_ids: Optional[List[int]] = None

class InvoiceUpdate(BaseModel):
    invoice_number: Optional[str]
    client_name: Optional[str]
    description: Optional[str]
    amount: Optional[float]
    issued_at: Optional[datetime]
    due_date: Optional[datetime]
    paid: Optional[bool]
    task_ids: Optional[List[int]]

class InvoiceRead(InvoiceBase):
    id: int
    tasks: List[TaskRead] = []

    class Config:
        orm_mode = True