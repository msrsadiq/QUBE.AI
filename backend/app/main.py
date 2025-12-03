"""
Qube.AI FastAPI Application
----------------------------
Main application entry point for the Qube.AI backend API.

This module:
- Initializes the FastAPI application
- Configures CORS middleware for frontend communication
- Registers all API routers (auth, projects, LLM configs)
- Creates database tables on startup
- Provides health check endpoints

Application Architecture:
    - FastAPI for REST API framework
    - SQLAlchemy for ORM and database operations
    - JWT for authentication
    - Pydantic for request/response validation

API Documentation:
    - Swagger UI: http://localhost:8000/docs
    - ReDoc: http://localhost:8000/redoc
    - OpenAPI JSON: http://localhost:8000/openapi.json

Environment:
    Development: uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
    Production: Use gunicorn with uvicorn workers
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, projects
from app.api.routes import llm_config
from app.core.config import settings
from app.core.database import engine, Base

# Create all database tables
# This will create tables if they don't exist (safe for development)
# In production, use Alembic migrations instead
Base.metadata.create_all(bind=engine)

# Initialize FastAPI application with metadata
app = FastAPI(
    title=settings.APP_NAME,
    description="Agentic AI Testing Platform - Backend API for multi-agent QA automation",
    version=settings.APP_VERSION,
    docs_url="/docs",  # Swagger UI
    redoc_url="/redoc",  # ReDoc documentation
    contact={
        "name": "Qube.AI Team",
        "email": "support@qubeai.com"
    },
    license_info={
        "name": "Proprietary",
        "url": "https://qubeai.com/license"
    }
)

# Configure CORS middleware
# Allows frontend (Next.js on port 3000) to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js development server
        "http://127.0.0.1:3000"   # Alternative localhost address
    ],
    allow_credentials=True,  # Allow cookies and Authorization headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Register API routers
# All routes will be prefixed with /api
app.include_router(auth.router, prefix="/api")
app.include_router(projects.router, prefix="/api")
app.include_router(llm_config.router, prefix="/api")


@app.get("/", tags=["Root"])
def root():
    """
    Root endpoint - API information.
    
    Returns basic information about the API.
    This endpoint doesn't require authentication.
    
    Returns:
        dict: API name, version, and status
        
    Example Response:
        {
            "message": f"{settings.APP_NAME} API",
            "version": settings.APP_VERSION,
            "status": "active"
        }
    """
    return {
        "message": "Qube.AI API",
        "version": "1.0.0",
        "status": "active"
    }


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint.
    
    Used by monitoring tools and container orchestrators
    to verify the API is running and responsive.
    
    Returns:
        dict: Health status
        
    Example Response:
        {"status": "healthy"}
        
    Use Cases:
        - Kubernetes liveness/readiness probes
        - Load balancer health checks
        - Monitoring systems
    """
    return {
            "status": "healthy",
            "version": settings.APP_VERSION
        }


# Optional: Add startup event for logging
@app.on_event("startup")
async def startup_event():
    """
    Application startup event.
    
    Executes when the application starts.
    Useful for:
    - Logging application start
    - Initializing connections
    - Loading configuration
    - Warming up caches
    """
    print("=" * 50)
    print("Qube.AI API Server Starting...")
    print("=" * 50)
    print("📋 API Documentation: http://localhost:8000/docs")
    print("🔐 Authentication: JWT tokens required for protected routes")
    print("🗄️  Database: SQLite (development) / PostgreSQL (production)")
    print("=" * 50)


# Optional: Add shutdown event for cleanup
@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event.
    
    Executes when the application stops.
    Useful for:
    - Closing database connections
    - Saving state
    - Cleanup operations
    - Logging shutdown
    """
    print("=" * 50)
    print("Qube.AI API Server Shutting Down...")
    print("=" * 50)

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