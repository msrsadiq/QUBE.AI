"""
Project Model
-------------
SQLAlchemy model for managing testing projects in Qube.AI.

This model handles:
- Project metadata (name, domain, brief, tech stack)
- Figma/design references
- Compliance requirements
- Version tracking and audit trails
- Relationships with users

Each project serves as a container for:
- Requirements and their analysis
- Generated test cases
- LLM configurations
- Testing agents (Requirement Analyzer, Test Case Generator, etc.)
"""

"""
Project Model
-------------
SQLAlchemy model for project management.

UPDATED: Added relationship with LLM configurations.
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Project(Base):
    """
    Project entity for organizing testing activities.
    
    Each project can have:
    - Multiple LLM configurations
    - Requirements and test cases (future phases)
    - Team members (future phases)
    
    Attributes:
        id: Auto-generated primary key
        name: Project name
        domain: Business domain (e.g., Healthcare, E-commerce)
        brief: Project description
        tech_stack: Technologies used in the project
        figma_url: URL to design prototypes
        figma_credentials: Encrypted credentials for Figma access
        compliances: Regulatory requirements (e.g., HIPAA, GDPR)
        created_by: User who created this project
        created_at: Creation timestamp
        updated_at: Last modification timestamp
    """
    
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    domain = Column(String(255), nullable=False)
    brief = Column(Text, nullable=False)
    tech_stack = Column(Text, nullable=True)
    figma_url = Column(String(500), nullable=True)
    figma_credentials = Column(Text, nullable=True)  # Encrypted
    compliances = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer, ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", back_populates="projects")
    llm_configs = relationship(
        "LLMConfig", 
        back_populates="project", 
        cascade="all, delete-orphan",
        order_by="desc(LLMConfig.created_at)"
    )
    
    def __repr__(self):
        """String representation for debugging."""
        return f"<Project(id={self.id}, name='{self.name}', domain='{self.domain}')>"