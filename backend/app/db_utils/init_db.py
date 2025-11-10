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
    - llm_configs: LLM configurations per project (future)

Note: This is a destructive operation in development.
      In production, use Alembic migrations instead.
"""

from app.core.database import engine, SessionLocal, Base
from app.models.user import User
from app.models.project import Project  # Import to register with Base
from app.core.security import get_password_hash

def init_db():
    """
    Initialize database with tables and default data.
    
    Steps:
    1. Drop all existing tables (clean slate)
    2. Create all tables from SQLAlchemy models
    3. Create default admin user
    
    Warning: This drops all existing data!
    """
    print("=" * 60)
    print("Initializing Qube.AI Database...")
    print("=" * 60)
    
    # Drop all existing tables
    print("\n🗑️  Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    print("✅ Existing tables dropped")
    
    # Create all tables
    print("\n🏗️  Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✅ Tables created successfully:")
    print("   - users")
    print("   - projects")
    print("   - llm_configs (if exists)")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.username == "Admin").first()
        
        if not existing_admin:
            # Create default admin user
            print("\n👤 Creating default admin user...")
            admin_user = User(
                username="Admin",
                email="admin@qubeai.com",
                hashed_password=get_password_hash("Admin"),
                is_active=True,
                is_admin=True
            )
            db.add(admin_user)
            db.commit()
            print("✅ Default admin user created")
            print("   Username: Admin")
            print("   Password: Admin")
            print("   ⚠️  Change password in production!")
        else:
            print("\n👤 Admin user already exists - skipping creation")
        
        print("\n" + "=" * 60)
        print("✅ Database initialization complete!")
        print("=" * 60)
        print("\n🚀 You can now start the backend server:")
        print("   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error during initialization: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    init_db()