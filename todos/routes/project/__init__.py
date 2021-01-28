from fastapi import APIRouter, Depends

from todos import schemas
from todos.dependencies import get_project
from todos.domain.entities import Project
from todos.routes.project import tasks

router = APIRouter(
    prefix="/{project_id}",
    dependencies=[Depends(get_project)],
)

router.include_router(tasks.router, tags=["tasks"])


@router.get("", response_model=schemas.Project, tags=["projects"])
def project_endpoint(project: Project = Depends(get_project)):
    return project
