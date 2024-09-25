from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskCardModel(BaseModel):
    title: str
    description: str
    is_private: bool
    id: int
    owner_id: int
    created_at: datetime
    is_completed: bool
    due_date: Optional[datetime]
    completed_at: Optional[datetime]


class TaskBaseModel(BaseModel):
    title: str
    description: str
    is_private: bool


class CreateTaskModel(TaskBaseModel):
    due_date: Optional[datetime]
    pass


class UpdateTaskModel(TaskBaseModel):
    due_date: Optional[datetime]
    is_completed: bool


class TaskResponseModel(TaskBaseModel):
    id: int
    owner_id: int
    created_at: datetime
    is_completed: bool
    due_date: Optional[datetime]
    completed_at: Optional[datetime]
