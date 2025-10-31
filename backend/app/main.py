from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
from datetime import datetime

# Import routers
from app.api.auth import router as auth_router
from app.api.projects import router as projects_router
from app.api.routes.llm_config import router as llm_config_router

# Import database
from app.core.database import init_db

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Qube.AI Backend API",
    description="Multi-Agent Agentic AI Application for Testing Activities",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js frontend
        "http://127.0.0.1:3000",
        "http://localhost:3001",  # Alternative port
        "*"  # Allow all origins in development (restrict in production)
    ],
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Initialize database on startup
@app.on_event("startup")
async def startup_event():
    """Initialize database on application startup"""
    logger.info("🚀 Starting Qube.AI Backend...")
    init_db()
    logger.info("✅ Database initialized successfully")
    logger.info("📝 API Documentation available at: http://localhost:8000/docs")

# Add middleware for logging
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests"""
    start_time = datetime.utcnow()
    
    # Log request
    logger.info(f"📥 Request: {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = (datetime.utcnow() - start_time).total_seconds()
    
    # Log response
    logger.info(f"📤 Response: {response.status_code} - Duration: {duration:.3f}s")
    
    return response

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to Qube.AI Backend API",
        "version": "1.0.0",
        "status": "running",
        "database": "SQLite",
        "timestamp": datetime.utcnow().isoformat(),
        "documentation": "/docs"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Qube.AI Backend",
        "database": "SQLite"
    }

# API info endpoint
@app.get("/api")
async def api_info():
    """API information endpoint"""
    return {
        "name": "Qube.AI API",
        "version": "1.0.0",
        "database": "SQLite",
        "endpoints": {
            "auth": "/api/auth",
            "projects": "/api/projects",
            "llm_config": "/api/llm-config",
            "health": "/health",
            "docs": "/docs"
        }
    }

# Include routers
app.include_router(auth_router)
app.include_router(projects_router)
app.include_router(llm_config_router)

# Exception handler for 404
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors"""
    return JSONResponse(
        status_code=404,
        content={
            "detail": "Not Found",
            "path": request.url.path,
            "method": request.method
        }
    )

# Exception handler for 500
@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {exc}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal Server Error",
            "message": "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )