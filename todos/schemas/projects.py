from todos.schemas.base_schema import BaseSchema


class Project(BaseSchema):
    id: int
    name: str
