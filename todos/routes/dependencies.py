from datetime import date, datetime

from fastapi import Depends, Path
from sqlalchemy.orm.session import Session

from todos.infrastructure.session import session_factory
from todos.models import Task, User
from todos.routes.errors import TaskNotFoundError, UserNotFoundError


def get_current_time() -> date:
    return datetime.utcnow()


def get_session():
    session = session_factory()

    try:
        yield session
    finally:
        session.close()


def get_user(
    user_id: int = Path(..., description="The ID of the user", ge=1),
    session: Session = Depends(get_session),
):
    user = session.query(User).get(user_id)

    if user is None:
        raise UserNotFoundError(user_id)

    return user


def get_task(
    task_id: int = Path(..., description="The ID of the task", ge=1),
    session: Session = Depends(get_session),
):
    task = session.query(Task).get(task_id)

    if task is None:
        raise TaskNotFoundError(task_id)

    return task
