"""
Database initialization utility.
Seeds default admin user for Phase 1.
"""

from sqlalchemy.orm import Session
from ..core.database import SessionLocal, engine, Base
from ..core.security import get_password_hash
from ..core.config import settings
from ..models.user import User


def create_admin_user(db: Session):
    """
    Create default admin user if it doesn't exist.
    
    Args:
        db: Database session
        
    Creates:
        Admin user with credentials from environment variables
        Default: username="Admin", password="Admin"
        
    Note:
        - Only creates user if username doesn't exist
        - Passwords are always hashed before storage
        - Safe to run multiple times (idempotent)
    """
    
    # Check if admin user already exists
    existing_user = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
    
    if existing_user:
        print(f"ℹ️  Admin user '{settings.ADMIN_USERNAME}' already exists")
        return
    
    # Create new admin user with hashed password
    admin_user = User(
        username=settings.ADMIN_USERNAME,
        hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
        full_name="System Administrator",
        is_active=True
    )
    
    db.add(admin_user)
    db.commit()
    db.refresh(admin_user)
    
    print(f"✅ Admin user '{settings.ADMIN_USERNAME}' created successfully")
    print(f"   Username: {settings.ADMIN_USERNAME}")
    print(f"   Password: {settings.ADMIN_PASSWORD}")
    print(f"   ⚠️  Change default password in production!")


def init_database():
    """
    Initialize database with tables and default data.
    
    Flow:
        1. Create all tables from models
        2. Seed default admin user
        
    Usage:
        Run this script directly or call from main.py startup event:
        python -m backend.app.db_utils.init_db
    """
    
    print("🔧 Initializing database...")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Seed default admin user
        create_admin_user(db)
    finally:
        db.close()
    
    print("🎉 Database initialization completed\n")


if __name__ == "__main__":
    """
    Allow script to be run directly for manual database initialization.
    
    Command:
        python -m backend.app.db_utils.init_db
    """
    init_database()