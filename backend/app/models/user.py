from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class SubscriptionStatus(str, Enum):
    trial = "trial"
    active = "active"
    lapsed = "lapsed"


class StoryIntensity(str, Enum):
    calm = "calm"
    moderate = "moderate"
    adventurous = "adventurous"


# ---------------------------------------------------------------------------
# User
# ---------------------------------------------------------------------------

class UserModel(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    email: str
    hashed_password: str
    family_name: str
    parent_passcode: str  # 4-digit PIN stored as string
    created_at: datetime = Field(default_factory=datetime.utcnow)
    subscription_status: SubscriptionStatus = SubscriptionStatus.trial
    subscription_expires_at: Optional[datetime] = None

    model_config = {"populate_by_name": True}


# ---------------------------------------------------------------------------
# Child Profile
# ---------------------------------------------------------------------------

class ChildProfile(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    name: str
    avatar: str  # emoji character or asset name, e.g. "🦄" or "avatar_unicorn"
    age: int
    allowed_themes: list[str] = Field(default_factory=list)
    blocked_themes: list[str] = Field(default_factory=list)
    story_intensity: StoryIntensity = StoryIntensity.calm
    sleep_timer_default: int = 20  # minutes
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_deleted: bool = False  # soft-delete flag

    model_config = {"populate_by_name": True}


# ---------------------------------------------------------------------------
# Voice Profile
# ---------------------------------------------------------------------------

class VoiceProfile(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    user_id: str
    child_profile_id: str
    label: str  # e.g. "Mom", "Dad", "Grandma"
    elevenlabs_voice_id: str
    recording_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}
