from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from todos import schemas
from todos.dependencies import get_session
from todos.domain.entities import Project
from todos.routes import project

router = APIRouter(prefix="/projects")

router.include_router(project.router)


@router.get(
    "",
    response_model=List[schemas.Project],
    name="Returns the list of all projects",
    tags=["projects"],
)
def projects_endpoint(session: Session = Depends(get_session)):
    return session.query(Project).all()
