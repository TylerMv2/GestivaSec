"""
Gestiva Security (GestivaSec V1) — Authentication REST API Router (SLICE-001 & SLICE-007)
Exposes /api/v1/auth/login, /api/v1/auth/me, and /api/v1/auth/logout endpoints.
"""
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status, Header
from pydantic import BaseModel, EmailStr, Field

from backend.application.auth_service import AuthenticationService

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])
auth_service = AuthenticationService()

class LoginRequest(BaseModel):
    email: EmailStr = Field(..., examples=["admin@gestivaone.com"])
    password: str = Field(..., examples=["GestivaSec2026!"])

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user_id: str
    organization_id: str
    email: str
    role: str

class UserProfileResponse(BaseModel):
    user_id: str
    organization_id: str
    email: str
    role: str
    is_active: bool

class MessageResponse(BaseModel):
    message: str

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(payload: LoginRequest):
    """Authenticates user credentials and issues a JWT access token."""
    try:
        user, token = await auth_service.authenticate_user(payload.email, payload.password)
        return TokenResponse(
            access_token=token,
            user_id=user.id,
            organization_id=user.organization_id,
            email=user.email,
            role=user.role
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(e))

@router.get("/me", response_model=UserProfileResponse)
async def get_current_user(authorization: Optional[str] = Header(None)):
    """Verifies Bearer JWT token and returns current authenticated user context."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Header Authorization Bearer requerido.")

    token = authorization.split(" ")[1]
    user = await auth_service.verify_token(token)

    if not user:
        raise HTTPException(status_code=401, detail="Token JWT inválido o expirado.")

    return UserProfileResponse(
        user_id=user.id,
        organization_id=user.organization_id,
        email=user.email,
        role=user.role,
        is_active=user.is_active
    )

@router.post("/logout", response_model=MessageResponse, status_code=status.HTTP_200_OK)
async def logout(authorization: Optional[str] = Header(None)):
    """Revokes current Bearer JWT token, adding it to the invalidation blacklist (BR-0005)."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Header Authorization Bearer requerido.")

    token = authorization.split(" ")[1]
    user = await auth_service.verify_token(token)

    if not user:
        raise HTTPException(status_code=401, detail="Token JWT ya invalidado o nulo.")

    await auth_service.revoke_token(token)
    return MessageResponse(message="Sesión cerrada exitosamente y token revocado.")
