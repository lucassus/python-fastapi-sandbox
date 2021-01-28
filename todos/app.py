from fastapi import FastAPI

from todos.infrastructure.tables import start_mappers
from todos.routes import api_router

start_mappers()


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)

    return app
