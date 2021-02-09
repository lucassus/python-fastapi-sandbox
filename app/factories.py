from typing import Optional

from app.models import User


def build_user(
    *,
    id: Optional[int] = None,
    email: str = "test@email.com",
) -> User:
    user = User(email=email, password="password")

    if id is not None:
        user.id = id

    return user
