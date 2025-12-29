"""
Main FastAPI Application
------------------------
Entry point for Qube.AI backend API.

UPDATED: Fixed model import order to resolve SQLAlchemy relationship issues.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

# CRITICAL: Import all models BEFORE creating tables
# This ensures SQLAlchemy knows about all models and their relationships
from app.models.user import User
from app.models.llm_config import LLMConfig  # Import BEFORE Project
from app.models.project import Project

from app.core.database import engine, Base

# Import routers
from app.api import auth, projects, llm_config

# Create database tables (models must be imported first)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Agentic AI Platform for Quality Engineering"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(llm_config.router)

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "message": f"{settings.APP_NAME} API",
        "version": settings.APP_VERSION,
        "status": "active"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION
    }


if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print(f"{settings.APP_NAME} API Server Starting...")
    print("="*50)
    print(f"📋 API Documentation: http://localhost:8000/docs")
    print(f"🔐 Authentication: JWT tokens required for protected routes")
    print(f"🗄️  Database: SQLite (development) / PostgreSQL (production)")
    print("="*50 + "\n")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)