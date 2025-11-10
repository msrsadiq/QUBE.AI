"""
Dependency Injection Utilities
------------------------------
Provides reusable dependencies for FastAPI routes.

Dependencies:
- get_db: Database session management
- get_current_user: Extract and validate authenticated user from JWT
- oauth2_scheme: OAuth2 password bearer token scheme

Usage in Routes:
    @router.get("/protected")
    def protected_route(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        return {"user": current_user.username}
"""

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import decode_access_token
from app.models.user import User


# OAuth2 scheme for token authentication
# tokenUrl points to the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency that extracts and validates the current authenticated user.
    
    Args:
        token: JWT token from Authorization header
        db: Database session
        
    Returns:
        User: Authenticated user object from database
        
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decode token
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception
    
    # Extract username from token
    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception
    
    # Fetch user from database
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user