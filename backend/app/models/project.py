from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.core.database import Base


class Project(Base):
    """Project model"""
    
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    domain = Column(String, nullable=False)
    brief = Column(Text, nullable=False)
    tech_stack = Column(Text)
    figma_url = Column(String)
    figma_credentials_encrypted = Column(Text)
    compliance = Column(Text)
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<Project(id={self.id}, name='{self.name}')>"


class ProjectSettings(Base):
    """Project-specific LLM settings"""
    
    __tablename__ = "project_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    project_id = Column(Integer, ForeignKey("projects.id"), unique=True)
    llm_provider = Column(String, default="ollama")
    llm_model = Column(String, default="llama2")
    api_key_encrypted = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    def __repr__(self):
        return f"<ProjectSettings(project_id={self.project_id}, provider='{self.llm_provider}')>"