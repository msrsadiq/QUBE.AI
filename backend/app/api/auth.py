"""
Authentication API endpoints.
Handles user login, logout, and current user information retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.core.dependencies import get_current_user
from app.models.user import User
from app.schemas.auth import LoginRequest, LoginResponse, UserResponse


# Router for authentication endpoints
router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=LoginResponse)
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and generate access token.
    
    Args:
        credentials: Login credentials (username and password)
        db: Database session
        
    Returns:
        LoginResponse: Access token and user information
        
    Raises:
        HTTPException 401: If credentials are invalid
    """
    
    # Fetch user from database
    user = db.query(User).filter(User.username == credentials.username).first()
    
    # Validate user exists and password is correct
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user account"
        )
    
    # Generate JWT access token
    access_token = create_access_token(data={"sub": user.username})
    
    # Return authentication response
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        username=user.username
    )


@router.post("/logout")
async def logout(
    current_user: User = Depends(get_current_user)
):
    """
    Logout current user.
    
    Note:
        JWT tokens are stateless, so actual logout is handled client-side
        by removing the token.
    """
    
    return {
        "message": "Successfully logged out",
        "username": current_user.username
    }


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: User = Depends(get_current_user)
):
    """
    Get current authenticated user's profile information.
    
    Args:
        current_user: Currently authenticated user from token
        
    Returns:
        UserResponse: User profile data
    """
    
    return UserResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        is_admin=current_user.is_admin
    )