import pytest
from fastapi import FastAPI
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import Session
from starlette.testclient import TestClient

from app.config import settings
from app.dependencies import get_session
from app.infrastructure.tables import create_tables, drop_tables, start_mappers
from app.routes import api_router

start_mappers()


@pytest.fixture
def db_engine():
    engine = create_engine(
        settings.database_url,
        connect_args={"check_same_thread": False},
    )

    create_tables(engine)
    yield engine
    drop_tables(engine)


@pytest.fixture
def db_connection(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()
    connection.close()


@pytest.fixture
def session(db_connection):
    session = Session(bind=db_connection)
    yield session
    session.close()


@pytest.fixture
def client(session):
    app = FastAPI()
    app.include_router(api_router)

    app.dependency_overrides[get_session] = lambda: session

    return TestClient(app=app)
