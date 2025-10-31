from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from app.core.database import Base

class Project(Base):
    """Project model"""
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Project Details
    name = Column(String(255), nullable=False, index=True)
    brief = Column(Text, nullable=False)
    domain = Column(String(255), nullable=False)
    tech_stack = Column(String(500), nullable=True)
    figma_url = Column(String(500), nullable=True)
    figma_credentials = Column(Text, nullable=True)  # Should be encrypted in production
    compliances = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="projects")
    llm_configs = relationship("LLMConfig", back_populates="project", cascade="all, delete-orphan")