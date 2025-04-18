from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Base schema for reading and creating tasks
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: Optional[str] = "pending"
    due_date: Optional[datetime] = None

# Schema for creating a task 
class TaskCreate(TaskBase): 
    pass

# Schema for updating a task
class TaskUpdate(TaskBase):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[datetime] = None

# Schema for reading a task
class TaskRead(TaskBase):
    id: int

    # Make it a response model
    class ConfigDict:
        from_attributes = True
