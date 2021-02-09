from datetime import date
from typing import Optional

from todos.models import Task, User


def build_user(
    *,
    id: Optional[int] = None,
    email: str = "test@email.com",
) -> User:
    user = User(email=email, password="password")

    if id is not None:
        user.id = id

    return user


def build_task(
    *,
    id: Optional[int] = None,
    name: str = "Test task",
    completed_at: Optional[date] = None,
) -> Task:
    task = Task(name=name, completed_at=completed_at)

    if id is not None:
        task.id = id

    return task
