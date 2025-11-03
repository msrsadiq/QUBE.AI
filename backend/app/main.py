"""
Main FastAPI application entry point.
Configures middleware, routes, and lifecycle events.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .core.database import init_db
from .api import auth


# Create FastAPI application instance
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Agentic AI Platform for Quality Engineers",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json"
)


# Configure CORS middleware for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_cors_origins(),  # Frontend URLs
    allow_credentials=True,  # Allow cookies and authorization headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)


# Include API routers
app.include_router(auth.router)


@app.on_event("startup")
async def startup_event():
    """
    Application startup event handler.
    
    Executes:
        - Database initialization (create tables)
        - Default admin user creation
        
    Note:
        Runs once when the application starts.
        Safe to run multiple times (idempotent).
    """
    init_db()
    print(f"✅ {settings.APP_NAME} v{settings.APP_VERSION} started successfully")
    print(f"📚 API Documentation: http://localhost:8000/api/docs")


@app.get("/")
async def root():
    """
    Root endpoint for health check.
    
    Returns:
        dict: Application name and version
        
    Usage:
        Verify the API is running and accessible
    """
    return {
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring and load balancers.
    
    Returns:
        dict: Service health status
        
    Future Enhancement:
        - Check database connectivity
        - Verify LLM service availability
        - Monitor system resources
    """
    return {
        "status": "healthy",
        "service": settings.APP_NAME
    }