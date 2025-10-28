from pydantic import BaseModel
from typing import Optional

class TaskBase(BaseModel):
    name: str
    completed: Optional[bool] = False

class TaskCreate(TaskBase):
    pass

class TaskUpdate(TaskBase):
    name: Optional[str] = None
    completed: Optional[bool] = None

class Task(TaskBase):
    id: int
    created_at: str

    class Config:
        orm_mode = True