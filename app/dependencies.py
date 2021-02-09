from datetime import date, datetime

from fastapi import Depends, Path
from sqlalchemy.orm.session import Session

from app.errors import TaskNotFoundError, UserNotFoundError
from app.infrastructure.session import session_factory
from app.models import Task, User


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


class CompleteTaskService:
    def __init__(
        self,
        session: Session = Depends(get_session),
        now: datetime = Depends(get_current_time),
    ):
        self._session = session
        self._now = now

    def __call__(self, task: Task):
        task.complete(self._now)
        self._session.commit()

        # TODO: Do some more complex stuff here...

        return task
