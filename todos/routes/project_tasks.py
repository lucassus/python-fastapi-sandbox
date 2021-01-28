from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from todos import schemas
from todos.common.errors import ProjectNotFoundError
from todos.dependencies import get_current_time, get_session
from todos.entities import Project

router = APIRouter()


@router.get("", response_model=List[schemas.Task], name="Returns list of tasks")
async def tasks_endpoint(
    project_id: int,
    session: Session = Depends(get_session),
):
    # TODO: Bring back types
    project = session.query(Project).get(project_id)

    if project is None:
        raise ProjectNotFoundError(id=project_id)

    return project.tasks


@router.post("", response_model=schemas.Task)
def task_create_endpoint(
    project_id: int,
    data: schemas.CreateTask,
    session: Session = Depends(get_session),
):
    # TODO: Create a dependency for project
    project: Project = session.query(Project).get(project_id)

    # TODO: Dry up 404 errors handling
    if project is None:
        raise ProjectNotFoundError(id=project_id)

    task = project.add_task(name=data.name)
    session.commit()

    return task


@router.get("/{id}", response_model=schemas.Task)
async def task_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task", ge=1),
    session: Session = Depends(get_session),
):
    project = session.query(Project).get(project_id)

    if project is None:
        raise ProjectNotFoundError(id=project_id)

    return project.get_task(id)


@router.put("/{id}/complete", response_model=schemas.Task)
def task_complete_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task to complete", ge=1),
    session: Session = Depends(get_session),
    now: date = Depends(get_current_time),
):
    project: Project = session.query(Project).get(project_id)

    if project is None:
        raise ProjectNotFoundError(id=id)

    task = project.complete_task(id, now=now)
    session.commit()

    return task


@router.put("/{id}/incomplete", response_model=schemas.Task)
def task_incomplete_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task to incomplete", ge=1),
    session: Session = Depends(get_session),
):
    project: Project = session.query(Project).get(project_id)

    if project is None:
        raise ProjectNotFoundError(id=id)

    task = project.incomplete_task(id)
    session.commit()

    return task
