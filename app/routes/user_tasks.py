from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.models import Task, User
from app.routes.dependencies import get_current_time, get_session, get_task, get_user

router = APIRouter(
    prefix="/users/{user_id}/tasks",
    dependencies=[Depends(get_user)],
)


@router.get(
    "",
    response_model=List[schemas.Task],
    name="Return list of user's tasks",
)
def tasks_endpoint(user: User = Depends(get_user)):
    return user.tasks


@router.post("", response_model=schemas.Task, name="Create a task")
def task_create_endpoint(
    data: schemas.CreateTask,
    user: User = Depends(get_user),
    session: Session = Depends(get_session),
):
    task = user.add_task(name=data.name)
    session.commit()

    return task


@router.get("/{task_id}", response_model=schemas.Task, name="Return a task by ID")
def task_endpoint(task=Depends(get_task)):
    return task


@router.put(
    "/{task_id}/complete",
    response_model=schemas.Task,
    name="Complete the task",
)
def task_complete_endpoint(
    task: Task = Depends(get_task),
    session: Session = Depends(get_session),
    now: date = Depends(get_current_time),
):
    task.completed_at = now
    session.commit()

    return task


@router.put(
    "/{task_id}/incomplete",
    response_model=schemas.Task,
    name="Incomplete the task",
)
def task_incomplete_endpoint(
    task: Task = Depends(get_task),
    session: Session = Depends(get_session),
):
    task.completed_at = None
    session.commit()

    return task
