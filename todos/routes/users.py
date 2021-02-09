from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from todos import schemas
from todos.models import User
from todos.routes.dependencies import get_session
from todos.routes.errors import UserNotFoundError

router = APIRouter(prefix="/users")


@router.post("", response_model=schemas.User)
def user_registration_endpoint(
    data: schemas.RegisterUser,
    session: Session = Depends(get_session),
):
    user = User(
        email=data.email,
        password=data.password,
    )
    session.add(user)
    session.commit()

    return user


@router.get(
    "/{id}",
    response_model=schemas.User,
    name="Returns the list of projects",
)
def user_endpoint(id: int, session: Session = Depends(get_session)):
    # TODO: Dry it
    user = session.query(User).get(id)

    if user is None:
        raise UserNotFoundError(id)

    return user
