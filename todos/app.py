from fastapi import FastAPI

from todos.infrastructure.tables import start_mappers
from todos.routes import api_router

start_mappers()

app = FastAPI()
app.include_router(api_router)
