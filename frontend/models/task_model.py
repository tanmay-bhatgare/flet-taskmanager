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
    is_completed: Optional[bool]
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
    completed_at: Optional[datetime]
    is_completed: Optional[bool]


class TaskResponseModel(TaskBaseModel):
    id: int
    owner_id: int
    created_at: datetime
    is_completed: Optional[bool | None]
    due_date: Optional[datetime]
    completed_at: Optional[datetime]


if __name__ == "__main__":
    task_response = TaskResponseModel(
        **{
            "id": 0,
            "title": "string",
            "description": "string",
            "is_private": True,
            "created_at": "2024-10-09T17:05:36.552Z",
            "due_date": "2024-10-09T17:05:36.552Z",
            "completed_at": "2024-10-09T17:05:36.552Z",
            "is_completed": True,
            "owner_id": 0,
        }
    )
    print(task_response.title)
