from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from todos import schemas
from todos.common.errors import TaskNotFoundError
from todos.dependencies import get_current_time, get_project, get_session
from todos.domain.entities import Project, Task

router = APIRouter(prefix="/tasks")


@router.get("", response_model=List[schemas.Task], name="Returns list of tasks")
def tasks_endpoint(
    project: Project = Depends(get_project),
):
    return project.tasks


@router.post("", response_model=schemas.Task)
def task_create_endpoint(
    data: schemas.CreateTask,
    project: Project = Depends(get_project),
    session: Session = Depends(get_session),
):
    task = project.add_task(name=data.name)
    session.commit()

    return task


@router.get("/{id}", response_model=schemas.Task)
def task_endpoint(
    id: int = Path(..., description="The ID of the task", ge=1),
    session: Session = Depends(get_session),
):
    task = session.query(Task).get(id)

    if task is None:
        raise TaskNotFoundError(id)

    return task


@router.put("/{id}/complete", response_model=schemas.Task)
def task_complete_endpoint(
    id: int = Path(..., description="The ID of the task to complete", ge=1),
    project: Project = Depends(get_project),
    session: Session = Depends(get_session),
    now: date = Depends(get_current_time),
):
    task = project.complete_task(id, now=now)
    session.commit()

    return task


@router.put("/{id}/incomplete", response_model=schemas.Task)
def task_incomplete_endpoint(
    id: int = Path(..., description="The ID of the task to incomplete", ge=1),
    project: Project = Depends(get_project),
    session: Session = Depends(get_session),
):
    task = project.incomplete_task(id)
    session.commit()

    return task
