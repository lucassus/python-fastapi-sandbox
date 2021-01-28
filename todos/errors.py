from fastapi import HTTPException, status


class EntityNotFoundError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class ProjectNotFoundError(EntityNotFoundError):
    def __init__(self, id: int):
        self.message = f"Unable to find a project with id={id}"


class TaskNotFoundError(EntityNotFoundError):
    def __init__(self, id: int):
        self.message = f"Unable to find a task with id={id}"


class MaxIncompleteTasksNumberIsReached(Exception):
    pass
