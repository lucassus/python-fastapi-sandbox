from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from todos.common.errors import EntityNotFoundError
from todos.infrastructure.tables import start_mappers
from todos.routes import api_router

start_mappers()


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(api_router)

    @app.exception_handler(EntityNotFoundError)
    async def unicorn_exception_handler(request: Request, exc: EntityNotFoundError):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": exc.message},
        )

    return app
