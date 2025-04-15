from pydantic import BaseModel
from typing import Optional


# Base schema for reading and creating tasks
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False

# Schema for creating a task 
class TaskCreate(TaskBase):
    pass

# Schema for reading a task
class TaskRead(TaskBase):
    id: int

    # Make it a response model
    class Config:
        orm_mode = True