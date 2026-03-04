from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from app.models.story import VoiceUsed


# ---------------------------------------------------------------------------
# Story Page Response
# ---------------------------------------------------------------------------

class StoryPageResponse(BaseModel):
    page_number: int
    text: str
    illustration_url: Optional[str] = None
    audio_url: Optional[str] = None


# ---------------------------------------------------------------------------
# Story Response
# ---------------------------------------------------------------------------

class StoryResponse(BaseModel):
    id: str
    title: str
    theme_tags: list[str]
    pages: list[StoryPageResponse]
    duration_seconds: int
    is_curated: bool
    is_ai_generated: bool
    created_for_child_id: Optional[str] = None
    created_at: datetime


# ---------------------------------------------------------------------------
# Story Generation Request
# ---------------------------------------------------------------------------

class GenerateStoryRequest(BaseModel):
    child_name: str = Field(min_length=1, max_length=50)
    themes: list[str] = Field(min_length=1, description="At least one theme required")
    child_profile_id: str
    voice: str = Field(
        default="ai",
        description="Voice to use: 'mom', 'dad', or 'ai'",
    )


# ---------------------------------------------------------------------------
# Session Requests / Responses
# ---------------------------------------------------------------------------

class StartSessionRequest(BaseModel):
    child_profile_id: str
    story_id: str
    voice_used: VoiceUsed = VoiceUsed.ai


class UpdateSessionRequest(BaseModel):
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = Field(default=None, ge=0)


class StorySessionResponse(BaseModel):
    id: str
    child_profile_id: str
    story_id: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    voice_used: VoiceUsed
