from typing import Optional
from pydantic import BaseModel, HttpUrl
from datetime import datetime

class ProjectBase(BaseModel):
    """Base project schema"""
    name: str
    brief: str
    domain: str
    tech_stack: Optional[str] = None
    compliances: Optional[str] = None

class ProjectCreate(ProjectBase):
    """Project creation schema"""
    figma_url: Optional[str] = None
    figma_credentials: Optional[str] = None

class ProjectUpdate(BaseModel):
    """Project update schema"""
    name: Optional[str] = None
    brief: Optional[str] = None
    domain: Optional[str] = None
    tech_stack: Optional[str] = None
    figma_url: Optional[str] = None
    figma_credentials: Optional[str] = None
    compliances: Optional[str] = None

class ProjectListResponse(ProjectBase):
    """Project list response schema"""
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ProjectResponse(ProjectBase):
    """Detailed project response schema"""
    id: int
    user_id: int
    figma_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        orm_mode = True

class ProjectStats(BaseModel):
    """Project statistics schema"""
    project_id: int
    project_name: str
    requirements_count: int
    test_cases_count: int
    bugs_count: int
    automation_scripts: int
    api_tests: int
    completion_percentage: float