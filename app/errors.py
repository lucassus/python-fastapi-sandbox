from fastapi import HTTPException, status


class EntityNotFoundError(HTTPException):
    def __init__(self, detail: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
        )


class UserNotFoundError(EntityNotFoundError):
    def __init__(self, id: int):
        super().__init__(detail=f"Unable to find a user with id={id}")


class TaskNotFoundError(EntityNotFoundError):
    def __init__(self, id: int):
        super().__init__(detail=f"Unable to find a task with id={id}")
