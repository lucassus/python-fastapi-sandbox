from typing import List

from sqlalchemy.orm import Session

from todos.domain.entities import Project


class ProjectsRepository:
    def __init__(self, session: Session):
        self._session = session

    def all(self) -> List[Project]:
        return self._session.query(Project).all()
