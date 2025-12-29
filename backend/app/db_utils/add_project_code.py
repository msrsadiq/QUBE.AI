"""
Migration Script: Add project_code to existing projects
--------------------------------------------------------
Run this if you have existing projects without project_code.
"""

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent.parent))

from app.core.database import SessionLocal
from app.models.project import Project
from sqlalchemy import text


def add_project_code_column():
    """Add project_code column to projects table if it doesn't exist."""
    db = SessionLocal()
    
    try:
        print("\n" + "="*60)
        print("Adding project_code column...")
        print("="*60 + "\n")
        
        # Check if column exists
        result = db.execute(text("PRAGMA table_info(projects)"))
        columns = [row[1] for row in result]
        
        if 'project_code' not in columns:
            print("📝 Adding project_code column...")
            db.execute(text("ALTER TABLE projects ADD COLUMN project_code VARCHAR(4)"))
            db.commit()
            print("✅ Column added\n")
        else:
            print("ℹ️  Column already exists\n")
        
        # Generate codes for existing projects
        print("🔢 Generating codes for existing projects...")
        projects = db.query(Project).filter(
            (Project.project_code == None) | (Project.project_code == '')
        ).all()
        
        if not projects:
            print("ℹ️  All projects already have codes\n")
        else:
            for project in projects:
                project.project_code = Project.generate_project_code(db)
                print(f"   Project ID {project.id}: {project.name} -> #{project.project_code}")
            
            db.commit()
            print(f"\n✅ Generated codes for {len(projects)} project(s)\n")
        
        print("="*60)
        print("✅ Migration complete!")
        print("="*60 + "\n")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    add_project_code_column()