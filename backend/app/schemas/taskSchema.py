from datetime import datetime
from ..models.taskModel import TaskStatus
from pydantic import BaseModel
from typing import Optional



class TaskBase(BaseModel):
    title: str
    description: str
    is_private: bool

class CreateTask(TaskBase):
    pass

class UpdateTask(TaskBase):
    status: TaskStatus
    due_date: Optional[datetime]
    completed_at: Optional[datetime]

class TaskResponse(TaskBase):
    id: int
    owner_id: int
    status: TaskStatus
    created_at: datetime
    due_date: Optional[datetime]
    completed_at: Optional[datetime]