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

    return project.task


@router.post("")
def task_create_endpoint(
    project_id: int,
    data: schemas.CreateTask,
):
    pass


@router.get("/{id}", response_model=schemas.Task)
async def task_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task", ge=1),
    session: Session = Depends(get_session),
):
    project = session.query(Project).get(project_id)

    if project is None:
        raise ProjectNotFoundError(id=id)

    return project.get_task(id)


@router.put("/{id}/complete")
def task_complete_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task to complete", ge=1),
    now: date = Depends(get_current_time),
):
    pass
    # service.complete_task(id, project_id=project_id, now=now)
    #
    # return RedirectResponse(
    #     f"/projects/{project_id}/tasks/{id}",
    #     status_code=status.HTTP_303_SEE_OTHER,
    # )


@router.put("/{id}/incomplete")
def task_incomplete_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task to incomplete", ge=1),
):
    pass
    # service.incomplete_task(id, project_id=project_id)
    #
    # return RedirectResponse(
    #     f"/projects/{project_id}/tasks/{id}",
    #     status_code=status.HTTP_303_SEE_OTHER,
    # )
