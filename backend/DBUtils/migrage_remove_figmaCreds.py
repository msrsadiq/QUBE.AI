"""
Database Migration: Remove figma_credentials column from projects table.
Run this after updating the project model to remove figma_credentials.
"""
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text, inspect
from app.core.config import settings

def check_column_exists(engine, table_name, column_name):
    """Check if a column exists in a table."""
    inspector = inspect(engine)
    columns = [col['name'] for col in inspector.get_columns(table_name)]
    return column_name in columns

def remove_figma_credentials_column():
    """Remove figma_credentials column if it exists."""
    print("=" * 70)
    print("🔄 Database Migration: Remove figma_credentials Column")
    print("=" * 70)
    
    try:
        engine = create_engine(settings.DATABASE_URL)
        
        # Check if column exists
        if check_column_exists(engine, 'projects', 'figma_credentials'):
            print("\n⚠️  Found 'figma_credentials' column in projects table")
            print("   Removing column...")
            
            with engine.connect() as conn:
                # Remove the column
                conn.execute(text("""
                    ALTER TABLE projects 
                    DROP COLUMN IF EXISTS figma_credentials
                """))
                conn.commit()
                
            print("   ✅ Column removed successfully")
        
        elif check_column_exists(engine, 'projects', 'figma_credentials_encrypted'):
            print("\n⚠️  Found 'figma_credentials_encrypted' column in projects table")
            print("   Removing column...")
            
            with engine.connect() as conn:
                # Remove the column
                conn.execute(text("""
                    ALTER TABLE projects 
                    DROP COLUMN IF EXISTS figma_credentials_encrypted
                """))
                conn.commit()
                
            print("   ✅ Column removed successfully")
        
        else:
            print("\n✓ No figma_credentials column found - already clean!")
        
        # Verify current schema
        print("\n📋 Current projects table columns:")
        inspector = inspect(engine)
        columns = inspector.get_columns('projects')
        for col in columns:
            print(f"   - {col['name']} ({col['type']})")
        
        print("\n✅ Migration completed successfully!")
        print("\n💡 Next steps:")
        print("   1. Restart your backend server")
        print("   2. Test project creation from UI")
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("\n💡 If table doesn't exist, run: python create_tables.py")
        return False
    
    print("\n" + "=" * 70)
    return True

if __name__ == "__main__":
    success = remove_figma_credentials_column()
    sys.exit(0 if success else 1)