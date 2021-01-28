from typing import List

from fastapi import APIRouter

from todos import schemas

router = APIRouter()


@router.get(
    "",
    response_model=List[schemas.Project],
    name="Returns the list of projects",
)
async def projects_endpoint():
    pass


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
