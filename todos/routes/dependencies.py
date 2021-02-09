from datetime import date, datetime

from fastapi import Path, Depends
from sqlalchemy.orm.session import Session

from todos.domain.entities import Project, Task
from todos.infrastructure.session import session_factory
from todos.routes.errors import ProjectNotFoundError, TaskNotFoundError


def get_current_time() -> date:
    return datetime.utcnow()


def get_session():
    session = session_factory()

    try:
        yield session
    finally:
        session.close()


def get_project(
    project_id: int = Path(..., description="The ID of the project", ge=1),
    session: Session = Depends(get_session),
) -> Project:
    project = session.query(Project).get(project_id)

    if project is None:
        raise ProjectNotFoundError(project_id)

    return project


def get_task(
    id: int = Path(..., description="The ID of the task", ge=1),
    session: Session = Depends(get_session),
):
    task = session.query(Task).get(id)

    if task is None:
        raise TaskNotFoundError(id)

    return task
