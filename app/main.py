from fastapi import FastAPI

from app.db.tables import start_mappers
from app.routes import api_router

start_mappers()

app = FastAPI()
app.include_router(api_router)
