from fastapi import APIRouter

from todos.routes import health, user_tasks, users

api_router = APIRouter()

api_router.include_router(health.router)
api_router.include_router(users.router, tags=["users"])
api_router.include_router(user_tasks.router, tags=["tasks"])
