from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Path, status
from starlette.responses import RedirectResponse

from todos.services.project_management.domain.service import Service
from todos.services.project_management.entrypoints import schemas
from todos.services.project_management.entrypoints.dependencies import (
    get_current_time,
    get_service,
)

router = APIRouter()


@router.get("", response_model=List[schemas.Task], name="Returns list of tasks_table")
async def tasks_endpoint(
    project_id: int,
    database: Database = Depends(get_database),
):
    query = select([tasks_table]).where(tasks_table.c.project_id == project_id)
    return await database.fetch_all(query=query)

@router.post("")
def task_create_endpoint(
    project_id: int,
    data: schemas.CreateTask,
    service: Service = Depends(get_service),
):
    task_id = service.create_task(name=data.name, project_id=project_id)

    return RedirectResponse(
        f"/projects/{project_id}/tasks/{task_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get("/{id}", response_model=schemas.Task)
async def task_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task", ge=1),
    database: Database = Depends(get_database),
):
    query = select([tasks_table]).where(
        and_(
            tasks_table.c.project_id == project_id,
            tasks_table.c.id == id,
        )
    )
    row = await database.fetch_one(query=query)

    if row is None:
        raise EntityNotFoundError(detail=f"Unable to find a task with ID={id}")

    return row


@router.put("/{id}/complete")
def task_complete_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task to complete", ge=1),
    service: Service = Depends(get_service),
    now: date = Depends(get_current_time),
):
    service.complete_task(id, project_id=project_id, now=now)

    return RedirectResponse(
        f"/projects/{project_id}/tasks/{id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.put("/{id}/incomplete")
def task_incomplete_endpoint(
    project_id: int,
    id: int = Path(..., description="The ID of the task to incomplete", ge=1),
    service: Service = Depends(get_service),
):
    service.incomplete_task(id, project_id=project_id)

    return RedirectResponse(
        f"/projects/{project_id}/tasks/{id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )
