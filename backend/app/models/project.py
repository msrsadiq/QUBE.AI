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
- LLM configurations (Phase 3)
- Testing agents (Requirement Analyzer, Test Case Generator, etc.)
"""

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class Project(Base):
    """
    Project entity representing a testing project in Qube.AI.
    
    Attributes:
        id (int): Primary key, auto-incremented project identifier
        name (str): Project name (required, max 255 chars)
        domain (str): Domain/industry area (e.g., E-commerce, Healthcare)
        brief (str): Detailed project description and context
        tech_stack (str): Technologies used in the project (optional)
        figma_url (str): URL to Figma/design prototype (optional)
        figma_credentials (str): Encrypted credentials for Figma access
        compliances (str): Compliance requirements (GDPR, HIPAA, etc.)
        created_at (datetime): Project creation timestamp
        updated_at (datetime): Last modification timestamp
        created_by (int): Foreign key to User who created the project
        
    Relationships:
        owner: Many-to-one relationship with User model
    """
    
    __tablename__ = "projects"

    # Primary Key
    id = Column(
        Integer, 
        primary_key=True, 
        index=True,
        comment="Auto-incremented project identifier"
    )
    
    # Core Project Fields (Required)
    name = Column(
        String(255), 
        nullable=False, 
        index=True,
        comment="Project name (required)"
    )
    domain = Column(
        String(255), 
        nullable=False,
        comment="Domain/industry area (e.g., E-commerce, Healthcare)"
    )
    brief = Column(
        Text, 
        nullable=False,
        comment="Detailed project description and context"
    )
    
    # Optional Project Fields
    tech_stack = Column(
        Text, 
        nullable=True,
        comment="Technologies used (e.g., React, Node.js, PostgreSQL)"
    )
    figma_url = Column(
        String(500), 
        nullable=True,
        comment="URL to Figma/design prototype"
    )
    figma_credentials = Column(
        Text, 
        nullable=True,
        comment="Encrypted credentials for Figma access"
    )
    compliances = Column(
        Text, 
        nullable=True,
        comment="Compliance requirements (GDPR, HIPAA, SOC2, etc.)"
    )
    
    # Audit Fields
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        comment="Project creation timestamp"
    )
    updated_at = Column(
        DateTime(timezone=True), 
        onupdate=func.now(),
        comment="Last modification timestamp"
    )
    
    # Foreign Keys
    created_by = Column(
        Integer, 
        ForeignKey("users.id"),
        comment="User ID who created this project"
    )
    
    # Relationships
    owner = relationship(
        "User", 
        back_populates="projects"
    )
    
    # NOTE: LLMConfig relationship will be added in Phase 3
    # llm_configs = relationship(
    #     "LLMConfig", 
    #     back_populates="project", 
    #     cascade="all, delete-orphan",
    #     lazy="dynamic"
    # )

    def __repr__(self):
        """String representation of Project object."""
        return f"<Project(id={self.id}, name='{self.name}', domain='{self.domain}')>"