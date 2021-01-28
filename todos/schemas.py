from datetime import date
from typing import List, Optional

from pydantic import Field

from todos.common.base_schema import BaseSchema


class Project(BaseSchema):
    id: int
    name: str


class CreateTask(BaseSchema):
    name: str = Field(..., title="New task's name", min_length=4, max_length=32)


class Task(BaseSchema):
    id: int
    name: str
    completed_at: Optional[date]


class RegisterUser(BaseSchema):
    email: str = Field(..., title="User email address", min_length=4, max_length=32)
    password: str = Field(..., min_length=6)


class User(BaseSchema):
    id: int
    email: str
    password: str

    # TODO: Bring it back
    # projects: List[Project]
