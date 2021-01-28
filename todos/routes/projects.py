from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from todos import schemas
from todos.common.errors import EntityNotFoundError
from todos.dependencies import get_session
from todos.entities import Project

router = APIRouter()


@router.get(
    "",
    response_model=List[schemas.Project],
    name="Returns the list of projects",
)
async def projects_endpoint(session: Session = Depends(get_session)):
    return session.query(Project).all()


@router.get("/{id}", response_model=schemas.Project)
def project_endpoint(id: int, session: Session = Depends(get_session)):
    project = session.query(Project).get(id)

    if project is None:
        raise EntityNotFoundError(detail=f"Unable to find a project with ID={id}")

    return project
