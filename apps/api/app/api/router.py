from fastapi import APIRouter
from app.api import admin, auth, courses, learning

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(courses.router)
api_router.include_router(learning.router)
api_router.include_router(admin.router)
