from fastapi import FastAPI

from app.infrastructure.tables import start_mappers
from app.routes import api_router

start_mappers()

app = FastAPI()
app.include_router(api_router)
