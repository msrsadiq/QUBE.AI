#!/usr/bin/env python
"""
Quick setup script for Qube.AI with SQLite
Run this to initialize your database and create the admin user
"""

import sys
import os

# Add the backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.database import init_db

def main():
    """Initialize the SQLite database"""
    print("=" * 50)
    print("🚀 Qube.AI SQLite Setup")
    print("=" * 50)
    
    # Initialize database
    init_db()
    
    print("=" * 50)
    print("✅ Setup Complete!")
    print("=" * 50)
    print("\n📝 Next steps:")
    print("1. Run: python -m uvicorn app.main:app --reload")
    print("2. Open: http://localhost:8000/docs")
    print("3. Login with: admin/admin")
    print("\n🎉 Happy testing with Qube.AI!")

if __name__ == "__main__":
    main()