"""
Database Initialization Script
------------------------------
Creates all database tables and seeds default admin user.

This script:
- Drops existing tables (for clean development reset)
- Creates all tables based on SQLAlchemy models
- Seeds default admin user (Admin/Admin)

Usage:
    python -m app.db_utils.init_db

Models Created:
    - users: Authentication and user management
    - projects: Project information and metadata
    - UPDATED: Added LLMConfig model import for Phase 3.

Note: This is a destructive operation in development.
      In production, use Alembic migrations instead.
"""
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.database import engine, SessionLocal, Base
from app.core.security import get_password_hash
from app.core.config import settings
from app.models.user import User
from app.models.project import Project
from app.models.llm_config import LLMConfig  # ADDED for Phase 3


def init_db():
    """
    Initialize database with tables and seed data.
    
    Steps:
    1. Drop all existing tables (use with caution!)
    2. Create all tables from models
    3. Create default admin user
    4. Commit changes
    """
    print("\n" + "="*60)
    print("Initializing Qube.AI Database...")
    print("="*60 + "\n")
    
    # Drop all existing tables
    print("🗑️  Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Existing tables dropped\n")
    
    # Create all tables
    print("🏗️  Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    # List created tables
    table_names = Base.metadata.tables.keys()
    print("✅ Tables created successfully:")
    for table_name in table_names:
        print(f"   - {table_name}")
    print()
    
    # Create default admin user
    print("👤 Creating default admin user...")
    db = SessionLocal()
    
    try:
        # Check if admin already exists
        admin_user = db.query(User).filter(User.username == settings.ADMIN_USERNAME).first()
        
        if not admin_user:
            admin_user = User(
                username=settings.ADMIN_USERNAME,
                hashed_password=get_password_hash(settings.ADMIN_PASSWORD),
                is_active=True
            )
            db.add(admin_user)
            db.commit()
            
            print("✅ Default admin user created")
            print(f"   Username: {settings.ADMIN_USERNAME}")
            print(f"   Password: {settings.ADMIN_PASSWORD}")
            print("   ⚠️  Change password in production!\n")
        else:
            print("ℹ️  Admin user already exists\n")
    
    except Exception as e:
        print(f"❌ Error creating admin user: {e}\n")
        db.rollback()
    
    finally:
        db.close()
    
    print("="*60)
    print("✅ Database initialization complete!")
    print("="*60 + "\n")
    print("🚀 You can now start the backend server:")
    print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000\n")


if __name__ == "__main__":
    init_db()