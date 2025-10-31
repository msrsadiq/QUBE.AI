"""
Verify all imports work correctly.
Run this before starting the backend to catch import errors early.
"""
import sys
from pathlib import Path

def test_imports():
    """Test all imports systematically."""
    print("=" * 70)
    print("🔍 Testing Backend Imports")
    print("=" * 70)
    
    errors = []
    
    # Test 1: Core imports
    print("\n1. Testing core imports...")
    try:
        from app.core.config import settings
        from app.core.database import Base, engine, get_db
        from app.core.security import verify_password, get_password_hash
        print("   ✅ Core imports OK")
    except Exception as e:
        print(f"   ❌ Core import error: {e}")
        errors.append(("Core", str(e)))
    
    # Test 2: Model imports
    print("\n2. Testing model imports...")
    try:
        from app.models.user import User
        from app.models.project import Project
        print("   ✅ Model imports OK")
    except Exception as e:
        print(f"   ❌ Model import error: {e}")
        errors.append(("Models", str(e)))
    
    # Test 3: Schema imports
    print("\n3. Testing schema imports...")
    try:
        from app.schemas.auth import LoginRequest, TokenResponse, UserInfo
        from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
        print("   ✅ Schema imports OK")
    except Exception as e:
        print(f"   ❌ Schema import error: {e}")
        errors.append(("Schemas", str(e)))
    
    # Test 4: API imports
    print("\n4. Testing API imports...")
    try:
        from app.api.auth import router as auth_router
        from app.api.projects import router as projects_router
        print("   ✅ API imports OK")
    except Exception as e:
        print(f"   ❌ API import error: {e}")
        errors.append(("API", str(e)))
    
    # Test 5: Main app import
    print("\n5. Testing main app import...")
    try:
        from app.main import app
        print("   ✅ Main app import OK")
    except Exception as e:
        print(f"   ❌ Main app import error: {e}")
        errors.append(("Main App", str(e)))
    
    print("\n" + "=" * 70)
    
    if errors:
        print("❌ IMPORT ERRORS FOUND!")
        print("\nErrors to fix:")
        for component, error in errors:
            print(f"\n{component}:")
            print(f"  {error}")
        print("\n💡 Fix these errors before starting the backend")
        print("=" * 70)
        return False
    else:
        print("✅ ALL IMPORTS SUCCESSFUL!")
        print("\nYour backend should start without errors now.")
        print("\n🚀 Run:")
        print("   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000")
        print("=" * 70)
        return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)