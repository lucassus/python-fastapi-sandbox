from datetime import date, datetime

from fastapi import Depends, Path
from sqlalchemy.orm import Session

from todos.common.errors import ProjectNotFoundError
from todos.entities import Project
from todos.infrastructure.session import session_factory


def get_current_time() -> date:
    return datetime.utcnow()


def get_session():
    session = session_factory()

    try:
        yield session
    finally:
        session.close()


# TODO: Move it to routes/projects?
def get_project(
    project_id: int = Path(..., description="The ID of the project", ge=1),
    session: Session = Depends(get_session),
) -> Project:
    project = session.query(Project).get(project_id)

    if project is None:
        raise ProjectNotFoundError(id=project_id)

    return project
