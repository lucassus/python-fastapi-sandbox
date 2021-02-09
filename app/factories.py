from app.models import User


def build_user(
    *,
    email: str = "test@email.com",
) -> User:
    return User(email=email, password="password")
