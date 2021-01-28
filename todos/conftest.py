import pytest
from fastapi import FastAPI
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from todos.dependencies import get_session
from todos.infrastructure.session import engine, session_factory
from todos.infrastructure.tables import create_tables, drop_tables, start_mappers
from todos.routes import api_router


@pytest.fixture(autouse=True, scope="module")
def create_test_database():
    create_tables(engine)
    yield
    drop_tables(engine)


@pytest.fixture
def session() -> Session:
    return session_factory()


@pytest.fixture
def client(session):
    app = FastAPI()
    app.include_router(api_router)

    app.dependency_overrides[get_session] = lambda: session

    return TestClient(app=app)


start_mappers()


# @pytest.fixture(scope="session")
# def db_engine() -> Engine:
#     database_path = os.path.join(os.path.dirname(__file__), "../../../todos_test.db")
#     engine = create_engine(
#         f"sqlite:///{database_path}", connect_args={"check_same_thread": False}
#     )
#
#     create_tables(engine)
#
#     return engine
#
#
# @pytest.fixture
# def db_connection(db_engine):
#     connection = db_engine.connect()
#     transaction = connection.begin()
#
#     yield connection
#
#     transaction.rollback()
#     connection.close()
#
#
# @pytest.fixture
# def session(request, db_connection):
#     if "integration" not in request.keywords:
#         raise AttributeError(
#             "Fixture session can be used only with tests marked as integration!"
#         )
#
#     session = Session(bind=db_connection)
#     yield session
#     session.close()
