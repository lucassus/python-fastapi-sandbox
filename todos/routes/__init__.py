from fastapi import APIRouter

from todos.routes import health, projects, tasks, users

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(users.router, tags=["users"])
api_router.include_router(projects.router)
api_router.include_router(tasks.router)
