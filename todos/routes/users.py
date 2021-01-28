from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from todos import schemas
from todos.dependencies import get_session
from todos.entities import User
from todos.errors import EntityNotFoundError

router = APIRouter()


@router.post("")
def user_register_endpoint(
    data: schemas.RegisterUser,
):
    pass
    # user_id = service.register_user(email=data.email, password=data.password)
    #
    # return RedirectResponse(
    #     f"/users/{user_id}",
    #     status_code=status.HTTP_303_SEE_OTHER,
    # )


@router.get(
    "/{id}",
    response_model=schemas.User,
    name="Returns the list of projects",
)
async def user_endpoint(id: int, session: Session = Depends(get_session)):
    user = session.query(User).get(id)
    if user is None:
        raise EntityNotFoundError(detail=f"Unable to find a user with ID={id}")

    return user
