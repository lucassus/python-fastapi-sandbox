from datetime import date
from typing import List

from fastapi import APIRouter, Depends, Path

from todos import schemas
from todos.dependencies import get_current_time

router = APIRouter()


@router.get("", response_model=List[schemas.Task], name="Returns list of tasks_table")
async def tasks_endpoint(project_id: int):
    pass


@router.post("")
def task_create_endpoint(
    project_id: int,
    data: schemas.CreateTask,
):
    pass


@router.get("/{id}", response_model=schemas.Task)
async def task_endpoint(
    project_id: int, id: int = Path(..., description="The ID of the task", ge=1)
):
    pass
    # query = select([tasks_table]).where(
    #     and_(
    #         tasks_table.c.project_id == project_id,
    #         tasks_table.c.id == id,
    #     )
    # )
    # row = await database.fetch_one(query=query)
    #
    # if row is None:
    #     raise EntityNotFoundError(detail=f"Unable to find a task with ID={id}")
    #
    # return row


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
