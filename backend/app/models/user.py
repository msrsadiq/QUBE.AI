"""
User Model
----------
SQLAlchemy model for user authentication and authorization.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base


class User(Base):
    """
    User entity for authentication and authorization.
    
    Attributes:
        id: Primary key
        username: Unique username for login
        email: User email address (optional for now)
        hashed_password: Bcrypt hashed password
        is_active: Account status flag
        is_admin: Admin privilege flag
        created_at: Account creation timestamp
    """
    
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False, index=True)
    email = Column(String(255), unique=True, nullable=True, index=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    
    def __repr__(self):
        """String representation for debugging."""
        return f"<User(id={self.id}, username='{self.username}')>"