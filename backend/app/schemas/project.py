from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    """Base project schema"""
    name: str
    domain: str
    brief: str
    tech_stack: Optional[str] = None
    figma_url: Optional[str] = None
    figma_credentials_encrypted: Optional[str] = None
    compliance: Optional[str] = None


class ProjectCreate(ProjectBase):
    """Project creation schema"""
    pass


class ProjectUpdate(BaseModel):
    """Project update schema"""
    name: Optional[str] = None
    domain: Optional[str] = None
    brief: Optional[str] = None
    tech_stack: Optional[str] = None
    figma_url: Optional[str] = None
    figma_credentials_encrypted: Optional[str] = None
    compliance: Optional[str] = None


class ProjectResponse(ProjectBase):
    """Project response schema"""
    id: int
    created_by: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True


class ProjectSettingsBase(BaseModel):
    """Base project settings schema"""
    llm_provider: str = "ollama"
    llm_model: str = "llama2"
    api_key_encrypted: Optional[str] = None


class ProjectSettingsCreate(ProjectSettingsBase):
    """Project settings creation schema"""
    project_id: int


class ProjectSettingsUpdate(BaseModel):
    """Project settings update schema"""
    llm_provider: Optional[str] = None
    llm_model: Optional[str] = None
    api_key_encrypted: Optional[str] = None


class ProjectSettingsResponse(ProjectSettingsBase):
    """Project settings response schema"""
    id: int
    project_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True