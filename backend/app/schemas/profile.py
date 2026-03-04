from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.user import StoryIntensity


# ---------------------------------------------------------------------------
# Child Profile Requests
# ---------------------------------------------------------------------------

class CreateChildProfileRequest(BaseModel):
    name: str = Field(min_length=1, max_length=50)
    avatar: str = Field(
        min_length=1,
        max_length=100,
        description="Emoji character or asset name, e.g. '🦄' or 'avatar_unicorn'",
    )
    age: int = Field(ge=1, le=12)
    allowed_themes: list[str] = Field(default_factory=list)
    blocked_themes: list[str] = Field(default_factory=list)
    story_intensity: StoryIntensity = StoryIntensity.calm
    sleep_timer_default: int = Field(default=20, ge=5, le=120)


class UpdateChildProfileRequest(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=50)
    avatar: Optional[str] = Field(default=None, min_length=1, max_length=100)
    age: Optional[int] = Field(default=None, ge=1, le=12)
    allowed_themes: Optional[list[str]] = None
    blocked_themes: Optional[list[str]] = None
    story_intensity: Optional[StoryIntensity] = None
    sleep_timer_default: Optional[int] = Field(default=None, ge=5, le=120)


# ---------------------------------------------------------------------------
# Child Profile Response
# ---------------------------------------------------------------------------

class ChildProfileResponse(BaseModel):
    id: str
    user_id: str
    name: str
    avatar: str
    age: int
    allowed_themes: list[str]
    blocked_themes: list[str]
    story_intensity: StoryIntensity
    sleep_timer_default: int
    created_at: datetime


# ---------------------------------------------------------------------------
# Voice Profile Requests / Responses
# ---------------------------------------------------------------------------

class CreateVoiceProfileRequest(BaseModel):
    label: str = Field(
        min_length=1,
        max_length=50,
        description="Human-readable label, e.g. 'Mom', 'Dad', 'Grandma'",
    )
    elevenlabs_voice_id: str = Field(min_length=1)
    recording_url: Optional[str] = None


class VoiceProfileResponse(BaseModel):
    id: str
    user_id: str
    child_profile_id: str
    label: str
    elevenlabs_voice_id: str
    recording_url: Optional[str] = None
    created_at: datetime
