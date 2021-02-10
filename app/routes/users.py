from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.dependencies import get_session, get_user
from app.models import User

router = APIRouter(prefix="/users")


@router.post(
    "",
    response_model=schemas.User,
    name="Create user",
    deprecated=True,
)
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
)
def user_endpoint(user=Depends(get_user)):
    return user
