"""
User Model
----------
SQLAlchemy model for user authentication and authorization.

This model handles:
- User credentials (username, password)
- User roles and permissions
- Relationships with projects (one user can own multiple projects)
- Timestamps for audit trails

Default Admin User:
    Username: Admin
    Password: Admin (hashed using bcrypt)
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """
    User entity for authentication and authorization.
    
    Attributes:
        id (int): Primary key, auto-incremented user identifier
        username (str): Unique username for login (max 50 chars)
        email (str): Optional unique email address for future use
        hashed_password (str): Bcrypt hashed password (255 chars)
        is_active (bool): Flag to enable/disable user access
        is_admin (bool): Flag to grant admin privileges
        created_at (datetime): Timestamp when user was created
        
    Relationships:
        projects: One-to-many relationship with Project model
                  User can own multiple projects
    """
    
    __tablename__ = "users"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)
    
    # Authentication Fields
    username = Column(
        String(50), 
        unique=True, 
        nullable=False, 
        index=True,
        comment="Unique username for login"
    )
    email = Column(
        String(100), 
        unique=True, 
        nullable=True, 
        index=True,
        comment="Email address (optional, for future use)"
    )
    hashed_password = Column(
        String(255), 
        nullable=False,
        comment="Bcrypt hashed password"
    )
    
    # Authorization Fields
    is_active = Column(
        Boolean, 
        default=True,
        comment="Flag to enable/disable user access"
    )
    is_admin = Column(
        Boolean, 
        default=False,
        comment="Flag to grant admin privileges"
    )
    
    # Audit Fields
    created_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(),
        comment="Timestamp when user was created"
    )
    
    # Relationships
    projects = relationship(
        "Project", 
        back_populates="owner",
        cascade="all, delete-orphan",
        lazy="dynamic"
    )

    def __repr__(self):
        """String representation of User object."""
        return f"<User(id={self.id}, username='{self.username}', is_admin={self.is_admin})>"