"""
Projects API Routes
------------------
CRUD operations for project management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import logging

from app.core.dependencies import get_db, get_current_user
from app.models.user import User
from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

# Setup logging
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/projects", tags=["Projects"])


@router.post("/", response_model=ProjectResponse, status_code=201)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new project with auto-generated 4-digit code."""
    # Generate unique project code
    project_code = Project.generate_project_code(db)
    logger.info(f"Generated project code: {project_code}")
    
    # Create project with generated code
    db_project = Project(
        project_code=project_code,
        **project_data.dict(),
        created_by=current_user.id
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Debug log
    logger.info(f"Created project: id={db_project.id}, code={db_project.project_code}, name={db_project.name}")
    
    return db_project


@router.get("/", response_model=List[ProjectResponse])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all projects for current user."""
    projects = db.query(Project).filter(
        Project.created_by == current_user.id
    ).order_by(Project.created_at.desc()).offset(skip).limit(limit).all()
    
    # Debug log
    for p in projects:
        logger.info(f"Project: id={p.id}, code={p.project_code}, name={p.name}")
    
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific project by ID."""
    project = db.query(Project).filter(
        Project.id == project_id,
        Project.created_by == current_user.id
    ).first()
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    logger.info(f"Retrieved project: id={project.id}, code={project.project_code}")
    
    return project


@router.put("/{project_id}", response_model=ProjectResponse)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update an existing project."""
    db_project = db.query(Project).filter(
        Project.id == project_id,
        Project.created_by == current_user.id
    ).first()
    
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Update only provided fields
    update_data = project_data.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    return db_project


@router.delete("/{project_id}", status_code=204)
async def delete_project(
    project_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a project."""
    db_project = db.query(Project).filter(
        Project.id == project_id,
        Project.created_by == current_user.id
    ).first()
    
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(db_project)
    db.commit()
    return None