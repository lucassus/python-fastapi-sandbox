from fastapi import Depends, Path
from sqlalchemy.orm.session import Session

from todos.domain.entities import Project, Task
from todos.routes.dependencies import get_session
from todos.routes.errors import ProjectNotFoundError, TaskNotFoundError


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
