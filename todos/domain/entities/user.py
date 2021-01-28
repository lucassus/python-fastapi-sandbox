from dataclasses import dataclass, field
from typing import List

from todos.domain.entities import Project


@dataclass
class User:
    id: int = field(init=False)
    email: str
    password: str

    projects: List[Project] = field(default_factory=list)
