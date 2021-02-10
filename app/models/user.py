from dataclasses import dataclass, field
from typing import List

from app.models.task import Task


@dataclass
class User:
    id: int = field(init=False)
    email: str
    password: str

    tasks: List[Task] = field(default_factory=list)

    def add_task(self, *, name: str) -> Task:
        task = Task(name=name)
        self.tasks.append(task)

        return task
