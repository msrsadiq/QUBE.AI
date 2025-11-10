"""
Project Schemas
---------------
Pydantic models for project data validation and serialization.

These schemas handle:
- Request validation (create/update operations)
- Response serialization (API responses)
- Data transformation between API and database layers

Schema Types:
    ProjectBase: Shared fields for all project operations
    ProjectCreate: Fields required for creating a new project
    ProjectUpdate: Fields allowed for updating an existing project
    ProjectResponse: Complete project data returned in API responses
    ProjectListResponse: Lightweight project data for list views
"""

from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ProjectBase(BaseModel):
    """
    Base schema with common project fields.
    
    This schema is inherited by ProjectCreate and defines the core
    fields that are common across create/update operations.
    
    Attributes:
        name: Project name (1-255 chars, required)
        domain: Domain/industry area (1-255 chars, required)
        brief: Project description (required, no length limit)
        tech_stack: Technologies used (optional)
        figma_url: Figma prototype URL (optional)
        figma_credentials: Encrypted Figma access credentials (optional)
        compliances: Compliance requirements (optional)
    """
    
    name: str = Field(
        ..., 
        min_length=1, 
        max_length=255,
        description="Project name (required)",
        examples=["E-commerce Platform", "Healthcare Portal"]
    )
    domain: str = Field(
        ..., 
        min_length=1, 
        max_length=255,
        description="Domain/industry area",
        examples=["E-commerce", "Healthcare", "FinTech"]
    )
    brief: str = Field(
        ..., 
        min_length=1,
        description="Detailed project description",
        examples=["Multi-vendor e-commerce platform with AI recommendations"]
    )
    tech_stack: Optional[str] = Field(
        None,
        description="Technologies used in the project",
        examples=["React, Node.js, PostgreSQL, Redis"]
    )
    figma_url: Optional[str] = Field(
        None,
        description="URL to Figma design prototype",
        examples=["https://figma.com/file/xyz123"]
    )
    figma_credentials: Optional[str] = Field(
        None,
        description="Credentials for accessing Figma (stored encrypted)",
        examples=["token:abc123xyz"]
    )
    compliances: Optional[str] = Field(
        None,
        description="Compliance requirements",
        examples=["GDPR, HIPAA, SOC2"]
    )


class ProjectCreate(ProjectBase):
    """
    Schema for creating a new project.
    
    Inherits all fields from ProjectBase. No additional fields needed
    as created_by is extracted from JWT token (authenticated user).
    
    Usage:
        POST /api/projects/
        Body: {"name": "...", "domain": "...", "brief": "..."}
    """
    pass


class ProjectUpdate(BaseModel):
    """
    Schema for updating an existing project.
    
    All fields are optional - only provided fields will be updated.
    This allows partial updates (PATCH semantics).
    
    Attributes:
        All fields from ProjectBase, but made optional
        
    Usage:
        PUT /api/projects/{id}
        Body: {"name": "Updated Name"}  # Only update name
    """
    
    name: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=255,
        description="Updated project name"
    )
    domain: Optional[str] = Field(
        None, 
        min_length=1, 
        max_length=255,
        description="Updated domain area"
    )
    brief: Optional[str] = Field(
        None, 
        min_length=1,
        description="Updated project description"
    )
    tech_stack: Optional[str] = Field(
        None,
        description="Updated tech stack"
    )
    figma_url: Optional[str] = Field(
        None,
        description="Updated Figma URL"
    )
    figma_credentials: Optional[str] = Field(
        None,
        description="Updated Figma credentials"
    )
    compliances: Optional[str] = Field(
        None,
        description="Updated compliance requirements"
    )


class ProjectResponse(ProjectBase):
    """
    Complete project data returned in API responses.
    
    Includes all project fields plus metadata (id, timestamps, owner).
    Used for single project retrieval (GET /api/projects/{id}).
    
    Attributes:
        All fields from ProjectBase plus:
        id: Project identifier
        created_at: Creation timestamp
        updated_at: Last modification timestamp
        created_by: User ID who created the project
    """
    
    id: int = Field(
        ...,
        description="Auto-generated project identifier",
        examples=[1, 42, 123]
    )
    created_at: datetime = Field(
        ...,
        description="Project creation timestamp"
    )
    updated_at: Optional[datetime] = Field(
        None,
        description="Last modification timestamp"
    )
    created_by: int = Field(
        ...,
        description="User ID who created this project",
        examples=[1]
    )

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True  # Allows creation from SQLAlchemy models


class ProjectListResponse(BaseModel):
    """
    Lightweight project data for list/card views.
    
    Contains only essential fields needed for displaying project cards
    in the home page. Reduces payload size for list endpoints.
    
    Used for:
        GET /api/projects/ - List all projects
        GET /api/projects/search?q=term - Search projects
    
    Attributes:
        id: Project identifier
        name: Project name
        domain: Domain area
        created_at: Creation timestamp (for sorting)
    """
    
    id: int = Field(
        ...,
        description="Project identifier",
        examples=[1, 42]
    )
    name: str = Field(
        ...,
        description="Project name",
        examples=["E-commerce Platform"]
    )
    domain: str = Field(
        ...,
        description="Domain area",
        examples=["E-commerce"]
    )
    created_at: datetime = Field(
        ...,
        description="Creation timestamp (for sorting by date)"
    )

    class Config:
        """Pydantic configuration for ORM mode."""
        from_attributes = True