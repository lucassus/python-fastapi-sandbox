from datetime import date
from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from todos import schemas
from todos.domain.entities import Project
from todos.routes.dependencies import get_current_time, get_session
from todos.routes.project.dependencies import get_project, get_task

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
def task_endpoint(task=Depends(get_task)):
    return task


@router.put(
    "/{id}/complete", response_model=schemas.Task, dependencies=[Depends(get_task)]
)
def task_complete_endpoint(
    id: int,
    project: Project = Depends(get_project),
    session: Session = Depends(get_session),
    now: date = Depends(get_current_time),
):
    task = project.complete_task(id, now=now)
    session.commit()

    return task


@router.put(
    "/{id}/incomplete", response_model=schemas.Task, dependencies=[Depends(get_task)]
)
def task_incomplete_endpoint(
    id: int,
    project: Project = Depends(get_project),
    session: Session = Depends(get_session),
):
    task = project.incomplete_task(id)
    session.commit()

    return task
