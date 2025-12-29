"""
Project Model
-------------
SQLAlchemy model for project management.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base
import random


class Project(Base):
    """
    Project entity for organizing testing activities.
    
    Attributes:
        id: Auto-generated primary key
        project_code: Unique 4-digit project identifier
        name: Project name
        domain: Business domain
        brief: Project description
        tech_stack: Technologies used
        figma_url: Design prototype URL
        figma_credentials: Encrypted Figma access credentials
        compliances: Regulatory requirements
        created_by: Owner user ID
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """
    
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    project_code = Column(String(4), unique=True, nullable=False, index=True)
    name = Column(String(255), nullable=False, index=True)
    domain = Column(String(255), nullable=False)
    brief = Column(Text, nullable=False)
    tech_stack = Column(Text, nullable=True)
    figma_url = Column(String(500), nullable=True)
    figma_credentials = Column(Text, nullable=True)
    compliances = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    
    @staticmethod
    def generate_project_code(db_session):
        """
        Generate a unique 4-digit project code.
        
        Args:
            db_session: SQLAlchemy session to check uniqueness
            
        Returns:
            Unique 4-digit code as string
        """
        while True:
            # Generate random 4-digit number (1000-9999)
            code = str(random.randint(1000, 9999))
            
            # Check if code already exists
            existing = db_session.query(Project).filter(
                Project.project_code == code
            ).first()
            
            if not existing:
                return code
    
    def __repr__(self):
        """String representation for debugging."""
        return f"<Project(id={self.id}, code='{self.project_code}', name='{self.name}')>"