"""
Script to create or update admin user with properly hashed password.
Run this script to fix the password hash issue.
"""
import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.user import User
from app.core.config import settings

# Password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def create_or_update_admin():
    """Create or update the admin user with properly hashed password."""
    # Create database connection
    engine = create_engine(settings.DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if admin user exists
        admin_user = db.query(User).filter(User.username == "Admin").first()
        
        # Hash the default password
        hashed_password = hash_password("Admin")
        
        if admin_user:
            # Update existing admin user
            admin_user.password_hash = hashed_password
            print(f"✓ Updated admin user password")
        else:
            # Create new admin user
            new_admin = User(
                username="Admin",
                password_hash=hashed_password,
                role="admin"
            )
            db.add(new_admin)
            print(f"✓ Created new admin user")
        
        # Commit the changes
        db.commit()
        
        print(f"\n✓ Admin credentials:")
        print(f"  Username: Admin")
        print(f"  Password: Admin")
        print(f"  Hashed password: {hashed_password[:50]}...")
        print(f"\n✓ You can now login with these credentials!")
        
    except Exception as e:
        print(f"✗ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Creating/Updating Admin User...")
    print("=" * 60)
    create_or_update_admin()
    print("=" * 60)