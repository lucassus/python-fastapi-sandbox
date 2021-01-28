import pytest
from fastapi import FastAPI
from httpx import AsyncClient

from todos.infrastructure.session import engine
from todos.infrastructure.tables import create_tables, drop_tables
from todos.routes import api_router


@pytest.fixture(autouse=True, scope="module")
def create_test_database():
    create_tables(engine)
    yield
    drop_tables(engine)


@pytest.fixture
def client():
    app = FastAPI()
    app.include_router(api_router)

    return AsyncClient(app=app, base_url="http://test")
