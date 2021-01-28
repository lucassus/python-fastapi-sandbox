from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from todos import schemas
from todos.common.errors import UserNotFoundError
from todos.dependencies import get_current_time, get_session
from todos.entities import Project, User

router = APIRouter()


@router.post("", response_model=schemas.User)
def user_registration_endpoint(
    data: schemas.RegisterUser,
    session: Session = Depends(get_session),
    now: date = Depends(get_current_time),
):
    user = User(email=data.email, password=data.password)
    session.add(user)

    project = Project(name="My first project")
    user.projects = [project]

    task = project.add_task(name="Sign up!")
    task.completed_at = now

    project.add_task(name="Watch the tutorial")
    project.add_task(name="Start using our awesome app")

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
        raise UserNotFoundError(id)

    return user
