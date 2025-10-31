from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
import os

# Import settings
try:
    from app.core.config import settings
    DATABASE_URL = settings.DATABASE_URL
except:
    # Fallback to environment variable or SQLite
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./qube_ai.db")

# SQLite configuration
if DATABASE_URL.startswith("sqlite"):
    # SQLite specific settings
    connect_args = {"check_same_thread": False}
    engine = create_engine(
        DATABASE_URL,
        connect_args=connect_args,
        echo=False,  # Set to True for SQL query logging
    )
    
    # Enable foreign key support for SQLite
    @event.listens_for(engine, "connect")
    def set_sqlite_pragma(dbapi_conn, connection_record):
        cursor = dbapi_conn.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()
else:
    # PostgreSQL or other databases (for future use)
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        echo=False,
    )

# Create SessionLocal class
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Create Base class for models
Base = declarative_base()

# Dependency to get DB session
def get_db() -> Generator[Session, None, None]:
    """
    Get database session.
    Usage: db: Session = Depends(get_db)
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
def init_db():
    """Initialize database and create all tables"""
    # Import all models here to ensure they are registered with Base
    from app.models import user, project, llm_config
    
    Base.metadata.create_all(bind=engine)
    print(f"✅ Database initialized: {DATABASE_URL}")
    
    # Create default admin user if not exists
    db = SessionLocal()
    try:
        from app.models.user import User
        from app.core.security import get_password_hash
        
        # Check if admin user exists
        admin_user = db.query(User).filter(User.username == "admin").first()
        if not admin_user:
            # Create admin user
            admin_user = User(
                username="admin",
                email="admin@qube.ai",
                hashed_password=get_password_hash("admin"),
                is_active=True,
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Default admin user created (admin/admin)")
    except Exception as e:
        print(f"Note: Could not create default user - {e}")
    finally:
        db.close()