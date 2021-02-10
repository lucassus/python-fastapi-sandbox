from datetime import date
from typing import Optional

from pydantic import Field

from app.schemas.base_schema import BaseSchema


class CreateTask(BaseSchema):
    name: str = Field(..., title="New task's name", min_length=6, max_length=32)


class Task(BaseSchema):
    id: int
    name: str
    completed_at: Optional[date]
