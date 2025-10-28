from fastapi import APIRouter
from .auth import router as auth_router
from .projects import router as projects_router

api_router = APIRouter()

# Include routers
api_router.include_router(auth_router, prefix="/auth", tags=["authentication"])
api_router.include_router(projects_router, prefix="/projects", tags=["projects"])

__all__ = ["api_router"]