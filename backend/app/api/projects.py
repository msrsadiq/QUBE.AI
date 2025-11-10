"""
Project API Routes
------------------
FastAPI router for project CRUD operations.

This module defines REST API endpoints for managing projects:
    POST   /api/projects/          - Create a new project
    GET    /api/projects/          - List all projects (paginated)
    GET    /api/projects/search    - Search projects by name/domain
    GET    /api/projects/{id}      - Get a specific project
    PUT    /api/projects/{id}      - Update a project
    DELETE /api/projects/{id}      - Delete a project

All routes require authentication (JWT token in Authorization header).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core.dependencies import get_db, get_current_user
from app.schemas.project import (
    ProjectCreate, 
    ProjectUpdate, 
    ProjectResponse,
    ProjectListResponse
)
from app.services.project_service import ProjectService
from app.models.user import User

# Create router with prefix and tags
router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Create a new project.
    
    Args:
        project: Project creation data
        db: Database session
        current_user: Authenticated user
        
    Returns:
        ProjectResponse: Created project with ID and timestamps
    """
    return ProjectService.create_project(db, project, current_user.id)


@router.get("/", response_model=List[ProjectListResponse])
def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all projects (paginated).
    
    Args:
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List[ProjectListResponse]: List of projects sorted by creation date
    """
    return ProjectService.get_projects(db, skip, limit)


@router.get("/search", response_model=List[ProjectListResponse])
def search_projects(
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Search projects by name or domain.
    
    Args:
        q: Search query string
        db: Database session
        current_user: Authenticated user
        
    Returns:
        List[ProjectListResponse]: Matching projects
    """
    return ProjectService.search_projects(db, q)


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific project by ID.
    
    Args:
        project_id: Project identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        ProjectResponse: Project details
        
    Raises:
        HTTPException 404: If project not found
    """
    project = ProjectService.get_project(db, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Update an existing project.
    
    Args:
        project_id: Project identifier
        project_update: Fields to update
        db: Database session
        current_user: Authenticated user
        
    Returns:
        ProjectResponse: Updated project
        
    Raises:
        HTTPException 404: If project not found
    """
    project = ProjectService.update_project(db, project_id, project_update)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Delete a project.
    
    Args:
        project_id: Project identifier
        db: Database session
        current_user: Authenticated user
        
    Returns:
        None (204 No Content)
        
    Raises:
        HTTPException 404: If project not found
    """
    success = ProjectService.delete_project(db, project_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Project with ID {project_id} not found"
        )
    return None