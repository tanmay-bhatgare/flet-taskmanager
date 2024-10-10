from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class TaskBase(BaseModel):
    title: str
    description: str
    is_private: bool


class CreateTask(TaskBase):
    due_date: Optional[datetime]


class UpdateTask(TaskBase):
    due_date: Optional[datetime]
    completed_at: Optional[datetime]


class TaskResponse(TaskBase):
    id: int
    owner_id: int
    created_at: datetime
    is_completed: Optional[bool]
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
