"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.api import auth, projects
from app.core.config import settings
from app.core.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI application
app = FastAPI(
    title="Qube.AI Backend API",
    description="Multi-Agent AI Testing Platform Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration - IMPORTANT for frontend-backend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js default dev server
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # Alternative port
        "http://127.0.0.1:3001",
        # Add your production URLs here when deploying
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers to the frontend
    max_age=3600,  # Cache preflight requests for 1 hour
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(projects.router, prefix="/api/v1/projects", tags=["Projects"])

@app.get("/")
async def root():
    """
    Root endpoint - API health check.
    """
    return {
        "message": "Qube.AI Backend API",
        "version": "1.0.0",
        "status": "operational",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring.
    """
    return {
        "status": "healthy",
        "database": "connected"
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """
    Global exception handler to catch and log all exceptions.
    """
    print(f"Global exception: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc)
        }
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """
    Application startup event.
    """
    print("=" * 60)
    print("🚀 Qube.AI Backend Starting...")
    print(f"📊 Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'PostgreSQL'}")
    print(f"🌐 Environment: {settings.ENVIRONMENT}")
    print(f"🔐 CORS Enabled for: http://localhost:3000")
    print("=" * 60)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """
    Application shutdown event.
    """
    print("=" * 60)
    print("👋 Qube.AI Backend Shutting Down...")
    print("=" * 60)