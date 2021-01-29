from datetime import date, datetime

from todos.infrastructure.session import session_factory


def get_current_time() -> date:
    return datetime.utcnow()


def get_session():
    session = session_factory()

    try:
        yield session
    finally:
        session.close()
