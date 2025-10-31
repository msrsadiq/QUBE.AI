"""
Password Hash Verification and Reset Tool
Use this to check if a password matches a hash or reset the admin password.
"""
import sys
from pathlib import Path
from passlib.context import CryptContext

# Password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Check if a password matches the hash."""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Error: {e}")
        return False

def main():
    """Main function."""
    print("=" * 70)
    print("🔐 Password Hash Verification Tool")
    print("=" * 70)
    
    # The hash from your database
    hash_from_db = "$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LeY5GyYzVEpTGzGO"
    
    print("\nHash from database:")
    print(f"  {hash_from_db}")
    
    # Common passwords to try
    common_passwords = [
        "Admin",
        "admin",
        "ADMIN", 
        "password",
        "Password",
        "123456",
        "postgres",
        "root",
        "admin123",
        "Admin123",
    ]
    
    print("\n🔍 Testing common passwords...")
    print("-" * 70)
    
    found = False
    for password in common_passwords:
        if verify_password(password, hash_from_db):
            print(f"✅ FOUND! The password is: {password}")
            found = True
            break
        else:
            print(f"❌ Not '{password}'")
    
    if not found:
        print("\n⚠️  Password not found in common list.")
        print("\n💡 Options:")
        print("   1. Try your own password:")
        print("      Run this script and modify the common_passwords list")
        print("   2. Reset the password using the database:")
        
    print("\n" + "=" * 70)
    print("\n📝 To reset the admin password:")
    print("-" * 70)
    print("Option 1 - Use SQL directly:")
    print("  1. Open psql or pgAdmin")
    print("  2. Connect to qubeai_db database")
    print("  3. Run this SQL:")
    print()
    print("     UPDATE users")
    print("     SET password_hash = '$2b$12$YOUR_NEW_HASH_HERE'")
    print("     WHERE username = 'Admin';")
    print()
    print("Option 2 - Use our Python script:")
    print("  1. Make sure you have database access")
    print("  2. Run: python scripts/reset_admin.py")
    print("=" * 70)

if __name__ == "__main__":
    main()