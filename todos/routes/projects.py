from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from todos import schemas
from todos.domain.entities import Project
from todos.routes.dependencies import get_project, get_session

router = APIRouter(prefix="/projects")


@router.get(
    "",
    response_model=List[schemas.Project],
    name="Returns the list of all projects",
    tags=["projects"],
)
def projects_endpoint(session: Session = Depends(get_session)):
    return session.query(Project).all()


@router.get("/{project_id}", response_model=schemas.Project, tags=["projects"])
def project_endpoint(project: Project = Depends(get_project)):
    return project
