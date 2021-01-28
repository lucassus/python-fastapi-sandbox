from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from todos import schemas
from todos.dependencies import get_session
from todos.entities import Project

router = APIRouter()


# TODO: Write an integration test
@router.get(
    "",
    response_model=List[schemas.Project],
    name="Returns the list of projects",
)
async def projects_endpoint(session: Session = Depends(get_session)):
    return session.query(Project).all()


@router.get("/{id}", response_model=schemas.Project)
async def project_endpoint(id: int):
    pass
    # query = select([projects_table]).where(projects_table.c.id == id)
    # row = await database.fetch_one(query=query)
    #
    # if row is None:
    #     raise EntityNotFoundError(detail=f"Unable to find a project with ID={id}")
    #
    # return row
