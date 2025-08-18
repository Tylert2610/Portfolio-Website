from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from ....core.rate_limiter import rate_limiter
from ....core.security import (create_access_token, verify_password,
                               verify_token)
from ....database import get_db
from ....models import User as UserModel
from ....schemas import Token, UserLogin

router = APIRouter()
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> UserModel:
    """Get current authenticated user"""
    token = credentials.credentials
    username = verify_token(token)
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = db.query(UserModel).filter(UserModel.username == username).first()
    if not user or not user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
    return user


@router.post("/login", response_model=Token)
async def login(user_credentials: UserLogin, db: Session = Depends(get_db)):
    """Admin login"""
    user = (
        db.query(UserModel)
        .filter(UserModel.username == user_credentials.username)
        .first()
    )
    if not user or not verify_password(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/rate-limit/stats", response_model=Dict)
async def get_rate_limit_stats(current_user: UserModel = Depends(get_current_user)):
    """Get global rate limiting statistics (admin only)"""
    return rate_limiter.get_global_stats()


@router.get("/rate-limit/client/{client_id}", response_model=Dict)
async def get_client_rate_limit_stats(
    client_id: str, current_user: UserModel = Depends(get_current_user)
):
    """Get rate limiting statistics for a specific client (admin only)"""
    return rate_limiter.get_client_stats(client_id)


@router.post("/rate-limit/client/{client_id}/reset")
async def reset_client_rate_limit(
    client_id: str, current_user: UserModel = Depends(get_current_user)
):
    """Reset rate limiting for a specific client (admin only)"""
    rate_limiter.reset_client(client_id)
    return {"message": f"Rate limiting reset for client: {client_id}"}
