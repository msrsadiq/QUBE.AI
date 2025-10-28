from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.core import get_db
from app.models import Project, ProjectSettings
from app.schemas import (
    ProjectCreate,
    ProjectUpdate,
    ProjectResponse,
    ProjectSettingsCreate,
    ProjectSettingsUpdate,
    ProjectSettingsResponse
)

router = APIRouter()


@router.get("/", response_model=List[ProjectResponse])
def get_all_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get all projects
    """
    projects = db.query(Project).offset(skip).limit(limit).all()
    return projects


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Get a specific project by ID
    """
    project = db.query(Project).filter(Project.id == project_id).first()
    
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    return project


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new project
    """
    # TODO: Get user_id from JWT token (for now using default 1)
    db_project = Project(
        **project.dict(),
        created_by=1
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    # Create default project settings
    default_settings = ProjectSettings(
        project_id=db_project.id,
        llm_provider="ollama",
        llm_model="llama2"
    )
    db.add(default_settings)
    db.commit()
    
    return db_project


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(
    project_id: int,
    project_update: ProjectUpdate,
    db: Session = Depends(get_db)
):
    """
    Update a project
    """
    db_project = db.query(Project).filter(Project.id == project_id).first()
    
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Update only provided fields
    update_data = project_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_project, field, value)
    
    db.commit()
    db.refresh(db_project)
    
    return db_project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Delete a project
    """
    db_project = db.query(Project).filter(Project.id == project_id).first()
    
    if not db_project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    # Delete associated settings
    db.query(ProjectSettings).filter(ProjectSettings.project_id == project_id).delete()
    
    # Delete project
    db.delete(db_project)
    db.commit()
    
    return None


@router.get("/{project_id}/settings", response_model=ProjectSettingsResponse)
def get_project_settings(
    project_id: int,
    db: Session = Depends(get_db)
):
    """
    Get project settings
    """
    settings = db.query(ProjectSettings).filter(
        ProjectSettings.project_id == project_id
    ).first()
    
    if not settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project settings not found"
        )
    
    return settings


@router.put("/{project_id}/settings", response_model=ProjectSettingsResponse)
def update_project_settings(
    project_id: int,
    settings_update: ProjectSettingsUpdate,
    db: Session = Depends(get_db)
):
    """
    Update project settings
    """
    db_settings = db.query(ProjectSettings).filter(
        ProjectSettings.project_id == project_id
    ).first()
    
    if not db_settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project settings not found"
        )
    
    # Update only provided fields
    update_data = settings_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_settings, field, value)
    
    db.commit()
    db.refresh(db_settings)
    
    return db_settings