from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.core import get_db, verify_password, create_access_token
from app.models import User
from app.schemas import LoginRequest, Token

router = APIRouter()


@router.post("/login", response_model=Token)
def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return access token
    """
    # Find user by username
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Create access token
    access_token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "role": user.role}
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }