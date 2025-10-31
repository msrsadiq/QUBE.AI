"""
Check Users and Fix Authentication Issues
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text
from app.core.config import settings

def check_users():
    """Check all users in database."""
    print("=" * 70)
    print("👥 Checking Users in Database")
    print("=" * 70)
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            # Get all users
            result = conn.execute(text("SELECT id, username, role, created_at FROM users ORDER BY id"))
            users = result.fetchall()
            
            if users:
                print(f"\n✅ Found {len(users)} user(s) in database:")
                print("-" * 70)
                for user in users:
                    print(f"   ID: {user[0]} | Username: {user[1]} | Role: {user[2]}")
                print("-" * 70)
                
                # Check if ID 1 exists
                has_id_1 = any(user[0] == 1 for user in users)
                if not has_id_1:
                    print("\n⚠️  WARNING: No user with ID=1 exists!")
                    print("   This is causing the foreign key error.")
                    
                    print("\n💡 Solution Options:")
                    print("   1. Update user ID sequence (recommended)")
                    print("   2. Create a user with ID=1")
                    print("   3. Fix authentication to use correct user ID")
                    
                    # Show which user IDs exist
                    existing_ids = [user[0] for user in users]
                    print(f"\n   Existing user IDs: {existing_ids}")
                    
                return users
            else:
                print("\n⚠️  No users found in database!")
                print("   Run: python reset_password.py to create admin user")
                return []
                
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return []
    
    finally:
        print("\n" + "=" * 70)

def fix_user_sequence():
    """Fix user ID sequence to match existing users."""
    print("\n" + "=" * 70)
    print("🔧 Fixing User ID Sequence")
    print("=" * 70)
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            # Get max user ID
            result = conn.execute(text("SELECT MAX(id) FROM users"))
            max_id = result.fetchone()[0]
            
            if max_id is None:
                print("\n⚠️  No users in database. Cannot fix sequence.")
                return False
            
            # Reset sequence to max_id + 1
            conn.execute(text(f"SELECT setval('users_id_seq', {max_id}, true)"))
            conn.commit()
            
            print(f"\n✅ Sequence fixed! Next user ID will be: {max_id + 1}")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Error fixing sequence: {e}")
        return False
    
    finally:
        print("=" * 70)

def create_user_with_id_1():
    """Create a dummy user with ID=1 if it doesn't exist."""
    print("\n" + "=" * 70)
    print("👤 Creating User with ID=1")
    print("=" * 70)
    
    try:
        from passlib.context import CryptContext
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            # Check if ID=1 exists
            result = conn.execute(text("SELECT id FROM users WHERE id = 1"))
            if result.fetchone():
                print("\n✓ User with ID=1 already exists")
                return True
            
            # Create user with ID=1
            hashed_password = pwd_context.hash("Admin")
            
            conn.execute(text("""
                INSERT INTO users (id, username, password_hash, role, created_at, updated_at)
                VALUES (1, 'SystemAdmin', :hash, 'admin', NOW(), NOW())
            """), {"hash": hashed_password})
            conn.commit()
            
            print(f"\n✅ Created system user with ID=1")
            print(f"   Username: SystemAdmin")
            print(f"   Password: Admin")
            
            return True
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False
    
    finally:
        print("=" * 70)

if __name__ == "__main__":
    users = check_users()
    
    if users:
        has_id_1 = any(user[0] == 1 for user in users)
        
        if not has_id_1:
            print("\n📋 Choose a fix:")
            print("   1. Create user with ID=1 (quick fix)")
            print("   2. Just show info and exit")
            
            choice = input("\nEnter choice (1-2): ").strip()
            
            if choice == "1":
                create_user_with_id_1()
                print("\n✅ Now restart your backend and try again!")
            else:
                print("\n💡 You can also:")
                print("   - Update your authentication code")
                print("   - Login again to get a new token")
                print("   - Use reset_password.py to manage users")