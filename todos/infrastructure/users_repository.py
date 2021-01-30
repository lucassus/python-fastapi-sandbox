from typing import Optional

from sqlalchemy.orm import Session

from todos.domain.entities import User


class UsersRepository:
    def __init__(self, session: Session):
        self._session = session

    def get(self, id: int) -> Optional[User]:
        return self._session.query(User).get(id)
