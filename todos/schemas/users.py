from typing import List

from pydantic import Field

from todos.schemas.base_schema import BaseSchema
from todos.schemas.projects import Project


class RegisterUser(BaseSchema):
    email: str = Field(..., title="User email address", min_length=4, max_length=32)
    password: str = Field(..., min_length=6)


class User(BaseSchema):
    id: int
    email: str
    password: str

    projects: List[Project]
