"""
Admin Password Reset Script
Run this to set a new password for the admin user.
"""
import sys
from pathlib import Path

# Add the parent directory to the path
sys.path.append(str(Path(__file__).parent.parent))

from passlib.context import CryptContext
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    return pwd_context.hash(password)

def reset_admin_password():
    """Reset the admin user password."""
    print("=" * 70)
    print("🔐 Admin Password Reset")
    print("=" * 70)
    
    # Get new password from user
    print("\nEnter new password for Admin user (or press Enter for 'Admin'):")
    new_password = input("> ").strip()
    
    if not new_password:
        new_password = "Admin"
        print("Using default password: Admin")
    
    # Hash the new password
    hashed_password = hash_password(new_password)
    print(f"\n✓ Password hashed successfully")
    print(f"  Hash: {hashed_password[:50]}...")
    
    # Create database connection
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            # Update the admin user's password
            result = conn.execute(
                text("UPDATE users SET password_hash = :hash WHERE username = 'Admin'"),
                {"hash": hashed_password}
            )
            conn.commit()
            
            if result.rowcount > 0:
                print(f"\n✅ SUCCESS! Admin password has been reset!")
                print(f"\n📋 New Login Credentials:")
                print(f"   Username: Admin")
                print(f"   Password: {new_password}")
                print(f"\n✓ You can now login with these credentials!")
            else:
                print(f"\n⚠️  No user found with username 'Admin'")
                print(f"   Creating new admin user...")
                
                # Create new admin user
                conn.execute(
                    text("""
                        INSERT INTO users (username, password_hash, role, created_at, updated_at)
                        VALUES (:username, :hash, 'admin', NOW(), NOW())
                    """),
                    {"username": "Admin", "hash": hashed_password}
                )
                conn.commit()
                
                print(f"\n✅ SUCCESS! Admin user created!")
                print(f"\n📋 Login Credentials:")
                print(f"   Username: Admin")
                print(f"   Password: {new_password}")
                
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"\n💡 Make sure:")
        print(f"   1. PostgreSQL is running")
        print(f"   2. Database 'qubeai_db' exists")
        print(f"   3. .env file has correct credentials")
        print(f"   4. Users table exists (run migrations first)")
        return False
    
    print("\n" + "=" * 70)
    return True

if __name__ == "__main__":
    reset_admin_password()