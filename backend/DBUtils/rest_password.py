"""
User Password Reset Script
Run this to reset password for any user in the system.
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

def list_users(conn):
    """List all users in the database."""
    try:
        result = conn.execute(text("SELECT id, username, role, created_at FROM users ORDER BY username"))
        users = result.fetchall()
        
        if users:
            print("\n📋 Current users in database:")
            print("-" * 70)
            for user in users:
                print(f"   ID: {user[0]} | Username: {user[1]} | Role: {user[2]} | Created: {user[3]}")
            print("-" * 70)
            return True
        else:
            print("\n⚠️  No users found in database")
            return False
    except Exception as e:
        print(f"\n⚠️  Could not list users: {e}")
        return False

def reset_user_password():
    """Reset password for any user."""
    print("=" * 70)
    print("🔐 User Password Reset Tool")
    print("=" * 70)
    
    # Create database connection
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as conn:
            # List existing users
            users_exist = list_users(conn)
            
            # Get username
            print("\nEnter username to reset (or press Enter for 'Admin'):")
            username = input("> ").strip()
            
            if not username:
                username = "Admin"
                print(f"Using default username: {username}")
            
            # Check if user exists
            result = conn.execute(
                text("SELECT id, username, role FROM users WHERE username = :username"),
                {"username": username}
            )
            existing_user = result.fetchone()
            
            if existing_user:
                print(f"\n✓ Found user: {existing_user[1]} (Role: {existing_user[2]})")
            else:
                print(f"\n⚠️  User '{username}' not found in database")
                
                # Ask if they want to create a new user
                print(f"\nDo you want to create a new user '{username}'? (yes/no):")
                create_new = input("> ").strip().lower()
                
                if create_new not in ['yes', 'y']:
                    print("\n❌ Operation cancelled")
                    return False
                
                # Get role for new user
                print("\nEnter role for new user (admin/user) [default: user]:")
                role = input("> ").strip().lower()
                if role not in ['admin', 'user']:
                    role = 'user'
                print(f"Role set to: {role}")
            
            # Get new password
            print(f"\nEnter new password for '{username}' (or press Enter for 'Admin'):")
            new_password = input("> ").strip()
            
            if not new_password:
                new_password = "Admin"
                print("Using default password: Admin")
            
            # Confirm password
            print("\nConfirm password:")
            confirm_password = input("> ").strip()
            
            if not confirm_password:
                confirm_password = "Admin"
            
            if new_password != confirm_password:
                print("\n❌ Passwords do not match! Operation cancelled.")
                return False
            
            # Hash the new password
            hashed_password = hash_password(new_password)
            print(f"\n✓ Password hashed successfully")
            print(f"  Hash: {hashed_password[:50]}...")
            
            if existing_user:
                # Update existing user's password
                result = conn.execute(
                    text("UPDATE users SET password_hash = :hash, updated_at = NOW() WHERE username = :username"),
                    {"hash": hashed_password, "username": username}
                )
                conn.commit()
                
                print(f"\n✅ SUCCESS! Password has been reset for user '{username}'!")
                
            else:
                # Create new user
                conn.execute(
                    text("""
                        INSERT INTO users (username, password_hash, role, created_at, updated_at)
                        VALUES (:username, :hash, :role, NOW(), NOW())
                    """),
                    {"username": username, "hash": hashed_password, "role": role}
                )
                conn.commit()
                
                print(f"\n✅ SUCCESS! New user '{username}' has been created!")
            
            print(f"\n📋 Login Credentials:")
            print(f"   Username: {username}")
            print(f"   Password: {new_password}")
            if not existing_user:
                print(f"   Role: {role}")
            print(f"\n✓ You can now login with these credentials!")
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print(f"\n💡 Troubleshooting:")
        print(f"   1. Make sure PostgreSQL is running")
        print(f"   2. Verify database 'qubeai_db' exists")
        print(f"   3. Check .env file has correct credentials")
        print(f"   4. Ensure users table exists:")
        print(f"      Run: python -c 'from app.core.database import Base, engine; Base.metadata.create_all(engine)'")
        return False
    
    print("\n" + "=" * 70)
    return True

def main():
    """Main function with menu."""
    while True:
        print("\n" + "=" * 70)
        print("🔐 User Password Management")
        print("=" * 70)
        print("\nOptions:")
        print("  1. Reset user password")
        print("  2. List all users")
        print("  3. Exit")
        print("\nSelect option (1-3):")
        
        choice = input("> ").strip()
        
        if choice == "1":
            reset_user_password()
            print("\nPress Enter to continue...")
            input()
        elif choice == "2":
            try:
                engine = create_engine(settings.DATABASE_URL)
                with engine.connect() as conn:
                    list_users(conn)
            except Exception as e:
                print(f"\n❌ Error: {e}")
            print("\nPress Enter to continue...")
            input()
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
        else:
            print("\n❌ Invalid option. Please select 1, 2, or 3.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
        sys.exit(0)