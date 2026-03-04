"""Authentication routes: register, login, and current-user."""

from datetime import datetime
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.deps import get_current_user, get_db
from app.core.security import create_access_token, hash_password, verify_password
from app.schemas.auth import (
    LoginRequest,
    RegisterRequest,
    TokenResponse,
    UserResponse,
)

router = APIRouter(prefix="/auth", tags=["auth"])


# ---------------------------------------------------------------------------
# POST /auth/register
# ---------------------------------------------------------------------------

@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: RegisterRequest,
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> TokenResponse:
    """Create a new family account and return a JWT access token."""
    # Check uniqueness
    existing = await db["users"].find_one({"email": payload.email})
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists.",
        )

    user_doc = {
        "email": payload.email,
        "hashed_password": hash_password(payload.password),
        "family_name": payload.family_name,
        "parent_passcode": payload.parent_passcode,
        "created_at": datetime.utcnow(),
        "subscription_status": "trial",
        "subscription_expires_at": None,
    }
    result = await db["users"].insert_one(user_doc)
    user_id = str(result.inserted_id)

    token = create_access_token({"sub": user_id})
    return TokenResponse(access_token=token)


# ---------------------------------------------------------------------------
# POST /auth/login
# ---------------------------------------------------------------------------

@router.post("/login", response_model=TokenResponse)
async def login(
    payload: LoginRequest,
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> TokenResponse:
    """Authenticate with email + password, return a JWT access token."""
    user = await db["users"].find_one({"email": payload.email})
    if user is None or not verify_password(payload.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
        )

    token = create_access_token({"sub": str(user["_id"])})
    return TokenResponse(access_token=token)


# ---------------------------------------------------------------------------
# GET /auth/me
# ---------------------------------------------------------------------------

@router.get("/me", response_model=UserResponse)
async def get_me(
    current_user: Annotated[dict, Depends(get_current_user)],
) -> UserResponse:
    """Return the currently authenticated user's profile."""
    return UserResponse(
        id=current_user["_id"],
        email=current_user["email"],
        family_name=current_user["family_name"],
        subscription_status=current_user["subscription_status"],
        subscription_expires_at=current_user.get("subscription_expires_at"),
        created_at=current_user["created_at"],
    )
