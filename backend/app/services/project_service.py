"""
Project Service Layer
--------------------
Business logic for project CRUD operations.

This service layer:
- Encapsulates database operations
- Provides reusable business logic
- Separates concerns from API routes
- Makes testing easier (can mock service layer)

Operations:
    - create_project: Create a new project
    - get_project: Retrieve a single project by ID
    - get_projects: Retrieve all projects (paginated, sorted)
    - update_project: Update existing project fields
    - delete_project: Delete a project (cascade to configs)
    - search_projects: Search projects by name or domain
"""

from sqlalchemy.orm import Session
from sqlalchemy import desc, or_
from typing import List, Optional
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


class ProjectService:
    """
    Service class for project-related business logic.
    
    All methods are static as they don't maintain state.
    Each method receives a database session and operates independently.
    """

    @staticmethod
    def create_project(
        db: Session, 
        project_data: ProjectCreate, 
        user_id: int
    ) -> Project:
        """
        Create a new project in the database.
        
        Args:
            db: SQLAlchemy database session
            project_data: Validated project creation data (Pydantic schema)
            user_id: ID of the user creating the project (from JWT token)
            
        Returns:
            Project: Newly created project with auto-generated ID
            
        Usage:
            project = ProjectService.create_project(db, project_data, user_id=1)
            
        Database Operations:
            1. Create Project instance from schema
            2. Set created_by to current user
            3. Add to session and commit
            4. Refresh to get auto-generated fields (id, created_at)
        """
        db_project = Project(
            **project_data.model_dump(),
            created_by=user_id
        )
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    def get_project(db: Session, project_id: int) -> Optional[Project]:
        """
        Retrieve a single project by ID.
        
        Args:
            db: SQLAlchemy database session
            project_id: Unique identifier of the project
            
        Returns:
            Project: Project object if found, None otherwise
            
        Usage:
            project = ProjectService.get_project(db, project_id=42)
            if not project:
                raise HTTPException(404, "Project not found")
        """
        return db.query(Project).filter(Project.id == project_id).first()

    @staticmethod
    def get_projects(
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Project]:
        """
        Retrieve all projects with pagination and sorting.
        
        Projects are sorted by created_at in descending order (newest first).
        This ensures the most recent projects appear at the top of the list.
        
        Args:
            db: SQLAlchemy database session
            skip: Number of records to skip (for pagination, default: 0)
            limit: Maximum number of records to return (default: 100)
            
        Returns:
            List[Project]: List of projects sorted by creation date (newest first)
            
        Usage:
            # Get first page (20 projects)
            projects = ProjectService.get_projects(db, skip=0, limit=20)
            
            # Get second page
            projects = ProjectService.get_projects(db, skip=20, limit=20)
            
        Note:
            For home page, typically use skip=0 and limit=100 to show all projects
        """
        return (
            db.query(Project)
            .order_by(desc(Project.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def update_project(
        db: Session, 
        project_id: int, 
        project_data: ProjectUpdate
    ) -> Optional[Project]:
        """
        Update an existing project with new data.
        
        Only provided fields are updated (partial update supported).
        The updated_at timestamp is automatically set by SQLAlchemy.
        
        Args:
            db: SQLAlchemy database session
            project_id: ID of project to update
            project_data: Validated update data (only provided fields)
            
        Returns:
            Project: Updated project object if found, None if not found
            
        Usage:
            # Update only the name
            update_data = ProjectUpdate(name="New Name")
            project = ProjectService.update_project(db, 42, update_data)
            
        Database Operations:
            1. Query project by ID
            2. Extract only provided fields (exclude_unset=True)
            3. Update each field dynamically
            4. Commit changes (updated_at auto-updated)
            5. Refresh to get latest data
        """
        # Find the project
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if not db_project:
            return None
        
        # Extract only provided fields (exclude None values)
        update_data = project_data.model_dump(exclude_unset=True)
        
        # Update each provided field
        for field, value in update_data.items():
            setattr(db_project, field, value)
        
        # Commit and refresh
        db.commit()
        db.refresh(db_project)
        return db_project

    @staticmethod
    def delete_project(db: Session, project_id: int) -> bool:
        """
        Delete a project and all its related data.
        
        Due to cascade delete configuration:
        - All LLM configs for this project are also deleted
        - Future: All requirements, test cases, etc. will be deleted
        
        Args:
            db: SQLAlchemy database session
            project_id: ID of project to delete
            
        Returns:
            bool: True if project was found and deleted, False if not found
            
        Usage:
            success = ProjectService.delete_project(db, project_id=42)
            if not success:
                raise HTTPException(404, "Project not found")
                
        Warning:
            This is a destructive operation. Consider implementing soft delete
            in production (is_deleted flag) instead of hard delete.
        """
        # Find the project
        db_project = db.query(Project).filter(Project.id == project_id).first()
        if not db_project:
            return False
        
        # Delete the project (cascade to related records)
        db.delete(db_project)
        db.commit()
        return True

    @staticmethod
    def search_projects(db: Session, search_term: str) -> List[Project]:
        """
        Search projects by name or domain (case-insensitive).
        
        Uses SQL ILIKE for case-insensitive partial matching.
        Results are sorted by creation date (newest first).
        
        Args:
            db: SQLAlchemy database session
            search_term: Search query string
            
        Returns:
            List[Project]: Projects matching the search term
            
        Usage:
            # Search for projects with "ecommerce" in name or domain
            results = ProjectService.search_projects(db, "ecommerce")
            
        Search Logic:
            - Matches if search_term appears anywhere in project name
            - OR matches if search_term appears anywhere in domain
            - Case-insensitive (converts both to lowercase)
            
        Example Matches:
            search_term="ecom"
            - Matches: "E-commerce Platform" (name)
            - Matches: "Shopping App" with domain "ecommerce"
            - Doesn't match: "Healthcare Portal"
        """
        search_pattern = f"%{search_term}%"
        return (
            db.query(Project)
            .filter(
                or_(
                    Project.name.ilike(search_pattern),
                    Project.domain.ilike(search_pattern)
                )
            )
            .order_by(desc(Project.created_at))
            .all()
        )