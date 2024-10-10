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
    due_date: Optional[datetime | str]


class UpdateTaskModel(TaskBaseModel):
    due_date: Optional[datetime | str]
    is_completed: Optional[bool]


class TaskResponseModel(TaskBaseModel):
    id: int
    owner_id: int
    created_at: datetime
    is_completed: bool
    due_date: Optional[datetime]
    completed_at: Optional[datetime]


if __name__ == "__main__":
    task_response = TaskResponseModel(
        **{
            "title": "string",
            "description": "string",
            "is_private": True,
            "id": 0,
            "owner_id": 0,
            "created_at": "2024-10-09T17:05:36.552Z",
            "is_completed": True,
            "due_date": "2024-10-09T17:05:36.552Z",
            "completed_at": "2024-10-09T17:05:36.552Z",
        }
    )
    print(task_response.title)
