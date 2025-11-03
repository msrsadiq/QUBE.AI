"""
User model representing authenticated users in the system.
Manages user credentials, profile information, and authentication state.
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from ..core.database import Base


class User(Base):
    """
    User model for authentication and authorization.
    
    Attributes:
        id: Primary key, auto-incrementing user identifier
        username: Unique username for login (e.g., "Admin")
        hashed_password: Bcrypt-hashed password, never stored in plain text
        full_name: Display name of the user (optional)
        is_active: Flag indicating if user account is active
        created_at: Timestamp of user creation
        updated_at: Timestamp of last user update
        
    Relationships:
        - Will be extended in future phases to include projects, settings, etc.
        
    Security:
        - Passwords are always hashed using bcrypt before storage
        - Plain passwords are never stored or logged
    """
    
    __tablename__ = "users"
    
    # Primary Key
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    
    # Authentication Fields
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # Profile Fields
    full_name = Column(String(100), nullable=True)
    
    # Status Fields
    is_active = Column(Boolean, default=True, nullable=False)
    
    # Audit Fields
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
    
    def __repr__(self):
        """String representation of User object for debugging."""
        return f"<User(id={self.id}, username='{self.username}', active={self.is_active})>"