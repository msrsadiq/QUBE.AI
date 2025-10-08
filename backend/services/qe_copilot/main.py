from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from api.v1 import requirements, test_cases, bugs, projects
from core.database import init_db, get_db
from config.settings import settings
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting QECopilot Backend Service...")
    await init_db()
    yield
    # Shutdown
    logger.info("Shutting down QECopilot Backend Service...")

app = FastAPI(
    title="QECopilot - Testing Agent Backend",
    version="1.0.0",
    description="AI-powered testing agent for comprehensive QA automation",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(projects.router, prefix="/api/v1/projects", tags=["projects"])
app.include_router(requirements.router, prefix="/api/v1/requirements", tags=["requirements"])
app.include_router(test_cases.router, prefix="/api/v1/test-cases", tags=["test_cases"])
app.include_router(bugs.router, prefix="/api/v1/bugs", tags=["bugs"])

@app.get("/")
async def root():
    return {
        "name": "QECopilot",
        "version": "1.0.0",
        "status": "operational"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}