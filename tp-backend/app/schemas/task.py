from pydantic import BaseModel
from typing import Optional

# ----- Task schemas -----
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    completed: Optional[bool]

class TaskRead(TaskBase):
    id: int

    class Config:
        orm_mode = True