"""
Database Connection Test Script
Run this to verify your database configuration before starting the backend.
"""
import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent))

from sqlalchemy import create_engine, text
from app.core.config import settings

def test_connection():
    """Test database connection with detailed feedback."""
    print("=" * 70)
    print("🔍 Testing Database Connection")
    print("=" * 70)
    
    print(f"\n📋 Configuration:")
    print(f"   Host: {settings.DB_HOST}")
    print(f"   Port: {settings.DB_PORT}")
    print(f"   Database: {settings.DB_NAME}")
    print(f"   User: {settings.DB_USER}")
    print(f"   Password: {'*' * len(settings.DB_PASSWORD)}")
    print(f"\n🔗 Connection String:")
    # Hide password in display
    safe_url = settings.DATABASE_URL.replace(settings.DB_PASSWORD, '****')
    print(f"   {safe_url}")
    
    print("\n🔄 Attempting connection...")
    
    try:
        # Create engine
        engine = create_engine(settings.DATABASE_URL)
        
        # Test connection
        with engine.connect() as conn:
            # Execute a simple query
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            
            # Get database name
            result = conn.execute(text("SELECT current_database()"))
            db_name = result.fetchone()[0]
            
            print("\n✅ SUCCESS! Database connection established!")
            print(f"\n📊 Database Info:")
            print(f"   Database: {db_name}")
            print(f"   PostgreSQL Version: {version.split(',')[0]}")
            
            print("\n✅ Your database is ready!")
            print("   You can now start the backend server:")
            print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
            
            return True
            
    except Exception as e:
        print("\n❌ FAILED! Database connection error!")
        print(f"\n📝 Error Details:")
        print(f"   {str(e)}")
        
        print("\n💡 Troubleshooting Steps:")
        
        error_msg = str(e).lower()
        
        if "password authentication failed" in error_msg:
            print("   ⚠️  Password is incorrect!")
            print("   1. Check your .env file")
            print("   2. Verify PostgreSQL password")
            print("   3. Update DB_PASSWORD in .env")
            
        elif "database" in error_msg and "does not exist" in error_msg:
            print("   ⚠️  Database doesn't exist!")
            print("   1. Open psql or pgAdmin")
            print("   2. Run: CREATE DATABASE qubeai_db;")
            print("   3. Try again")
            
        elif "connection refused" in error_msg or "could not connect" in error_msg:
            print("   ⚠️  PostgreSQL service is not running!")
            print("   1. Check if PostgreSQL is installed")
            print("   2. Start PostgreSQL service:")
            print("      - Windows: net start postgresql-x64-16")
            print("   3. Try again")
            
        elif "connection timed out" in error_msg:
            print("   ⚠️  Connection timeout!")
            print("   1. Check DB_HOST in .env (should be localhost or 127.0.0.1)")
            print("   2. Check DB_PORT in .env (usually 5432)")
            print("   3. Verify firewall settings")
            
        else:
            print("   ⚠️  Unknown error!")
            print("   1. Check all database credentials in .env")
            print("   2. Verify PostgreSQL is running")
            print("   3. See DATABASE_SETUP.md for detailed help")
        
        return False
        
    finally:
        print("\n" + "=" * 70)

if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)