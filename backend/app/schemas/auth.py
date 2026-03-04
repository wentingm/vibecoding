from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from app.models.user import SubscriptionStatus


# ---------------------------------------------------------------------------
# Requests
# ---------------------------------------------------------------------------

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)
    family_name: str = Field(min_length=1, max_length=100)
    parent_passcode: str = Field(
        pattern=r"^\d{4}$",
        description="4-digit numeric passcode for the parental dashboard",
    )


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# ---------------------------------------------------------------------------
# Responses
# ---------------------------------------------------------------------------

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    id: str
    email: str
    family_name: str
    subscription_status: SubscriptionStatus
    subscription_expires_at: Optional[datetime] = None
    created_at: datetime
