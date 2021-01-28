from fastapi import APIRouter, Depends, status
from starlette.responses import RedirectResponse

from todos.services.accounts.domain.service import Service
from todos.services.accounts.entrypoints import schemas
from todos.services.accounts.entrypoints.dependencies import get_service

router = APIRouter()


@router.post("")
def user_register_endpoint(
    data: schemas.RegisterUser,
    service: Service = Depends(get_service),
):
    user_id = service.register_user(email=data.email, password=data.password)

    return RedirectResponse(
        f"/users/{user_id}",
        status_code=status.HTTP_303_SEE_OTHER,
    )


@router.get(
    "/{id}",
    response_model=schemas.User,
    name="Returns the list of projects",
)
async def user_endpoint(id: int, database: Database = Depends(get_database)):
    query = select([users_table]).where(users_table.c.id == id)
    user = await database.fetch_one(query=query)

    if user is None:
        raise EntityNotFoundError(detail=f"Unable to find a user with ID={id}")

    query = select([projects_table]).where(projects_table.c.user_id == id)
    projects = await database.fetch_all(query=query)

    return dict(user, projects=[dict(project) for project in projects])
