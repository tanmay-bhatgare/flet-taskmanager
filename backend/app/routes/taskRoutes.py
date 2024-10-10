from typing import List
from fastapi import APIRouter, Request, Response, status, HTTPException, Depends
from sqlalchemy.orm import Session

from ..models import taskModel
from ..db.database import get_db
from ..schemas import taskSchema
from ..authentication.oauth2 import get_current_user
from ..utils.limiter import limiter


router = APIRouter(tags=["Tasks"], prefix="/tasks")


@router.get(
    "/", status_code=status.HTTP_200_OK, response_model=List[taskSchema.TaskResponse]
)
@limiter.limit("30/minute")
#! Retrieve All Tasks
def get_tasks(
    db: Session = Depends(get_db), current_user: Session = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Please Log In First."
        )

    tasks = (
        db.query(taskModel.Task)
        .filter(taskModel.Task.owner_id == current_user.id)
        .order_by(taskModel.Task.id)
        .all()
    )

    return tasks


@router.post(
    "/create",
    status_code=status.HTTP_201_CREATED,
    response_model=taskSchema.TaskResponse,
)
@limiter.limit("30/minute")
#! Create New Task
def create_task(
    request: Request,
    task: taskSchema.CreateTask,
    db: Session = Depends(get_db),
    current_user: Session = Depends(get_current_user),
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Please Log In First."
        )

    new_task = taskModel.Task(owner_id=current_user.id, **task.model_dump())
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@router.get(
    "/{id}", status_code=status.HTTP_200_OK, response_model=taskSchema.TaskResponse
)
@limiter.limit("30/minute")
#! Retrieve One Task By ID
def get_task(
    id: int,
    db: Session = Depends(get_db),
    current_user: Session = Depends(get_current_user),
):
    task = db.query(taskModel.Task).filter(taskModel.Task.id == id).first()

    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Please Log In First."
        )

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task Not Found"
        )

    if current_user.id != task.owner_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Action. Don't Have Permission To Perform Requested Action.",
        )

    return task


@router.delete("/delete/{id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("30/minute")
#! Delete Task By ID
def delete_task(
    id: int,
    db: Session = Depends(get_db),
    current_user: Session = Depends(get_current_user),
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Please Log In First."
        )

    delete_query = db.query(taskModel.Task).filter(taskModel.Task.id == id)
    deleted_task = delete_query.first()

    if deleted_task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task Not Found"
        )

    if current_user.id != deleted_task.owner_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Action. Don't Have Permission To Perform Requested Action.",
        )

    delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put(
    "/update/{id}",
    status_code=status.HTTP_200_OK,
    response_model=taskSchema.TaskResponse,
)
@limiter.limit("30/minute")
#! Update Task By ID
def update_task(
    task: taskSchema.UpdateTask,
    id: int,
    db: Session = Depends(get_db),
    current_user: Session = Depends(get_current_user),
):
    if current_user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Please Log In First."
        )

    update_query = db.query(taskModel.Task).filter(taskModel.Task.id == id)

    updated_task = update_query.first()

    if not updated_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Task Not Found"
        )

    if current_user.id != updated_task.owner_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unauthorized Action. Don't Have Permission To Perform Requested Action.",
        )

    update_query.update(task.model_dump(), synchronize_session=False)
    db.commit()
    return updated_task
