from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from todos import schemas
from todos.models import User
from todos.routes.dependencies import get_session, get_user

router = APIRouter(prefix="/users")


@router.post("", response_model=schemas.User, name="Create user")
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
    "/{user_id}",
    response_model=schemas.User,
    name="Return the user by ID",
    deprecated=True,
)
def user_endpoint(user=Depends(get_user)):
    return user
