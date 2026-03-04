from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.database import get_database
from app.core.security import verify_token

# ---------------------------------------------------------------------------
# HTTP Bearer scheme
# ---------------------------------------------------------------------------

bearer_scheme = HTTPBearer()


# ---------------------------------------------------------------------------
# Database dependency
# ---------------------------------------------------------------------------

async def get_db() -> AsyncIOMotorDatabase:
    """FastAPI dependency that returns the active MongoDB database instance."""
    return get_database()


# ---------------------------------------------------------------------------
# Auth dependency
# ---------------------------------------------------------------------------

async def get_current_user(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> dict:
    """FastAPI dependency that verifies the Bearer JWT and returns the user document.

    Raises HTTP 401 if the token is missing, invalid, or the user no longer exists.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = verify_token(credentials.credentials)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    from bson import ObjectId

    try:
        oid = ObjectId(user_id)
    except Exception:
        raise credentials_exception

    user = await db["users"].find_one({"_id": oid})
    if user is None:
        raise credentials_exception

    # Normalise _id to str for downstream use
    user["_id"] = str(user["_id"])
    return user
