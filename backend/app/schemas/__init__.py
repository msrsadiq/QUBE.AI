"""
Schemas package initialization.
Import all schemas here for easy access.
"""
from app.schemas.auth import LoginRequest, TokenResponse, UserInfo, TokenData
from app.schemas.project import ProjectCreate, ProjectUpdate, ProjectResponse

__all__ = [
    # Auth schemas
    "LoginRequest",
    "TokenResponse",
    "UserInfo",
    "TokenData",
    # Project schemas
    "ProjectCreate",
    "ProjectUpdate",
    "ProjectResponse",
]