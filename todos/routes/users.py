from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from todos import schemas
from todos.common.errors import EntityNotFoundError
from todos.dependencies import get_session
from todos.entities import User

router = APIRouter()


@router.post("", response_model=schemas.User)
def user_registration_endpoint(
    data: schemas.RegisterUser,
    session: Session = Depends(get_session),
):
    user = User(email=data.email, password=data.password)
    session.add(user)
    session.commit()

    return user


@router.get(
    "/{id}",
    response_model=schemas.User,
    name="Returns the list of projects",
)
def user_endpoint(id: int, session: Session = Depends(get_session)):
    user = session.query(User).get(id)
    if user is None:
        raise EntityNotFoundError(detail=f"Unable to find a user with ID={id}")

    return user
