"""
Database configuration and session management.
Provides SQLAlchemy engine, session factory, and base model class.
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    pool_pre_ping=True,  # Verify connections before using them
    echo=settings.DEBUG  # Log SQL statements in debug mode
)

# Session factory for creating database sessions
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base class for all SQLAlchemy models
Base = declarative_base()


def get_db():
    """
    Dependency function that provides database session to route handlers.
    
    Yields:
        Session: SQLAlchemy database session
        
    Ensures:
        Session is properly closed after request completion
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db():
    """
    Initialize database by creating all tables defined in models.
    Should be called on application startup.
    """
    Base.metadata.create_all(bind=engine)