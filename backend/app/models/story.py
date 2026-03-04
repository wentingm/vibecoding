from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class VoiceUsed(str, Enum):
    mom = "mom"
    dad = "dad"
    ai = "ai"


# ---------------------------------------------------------------------------
# Story Page
# ---------------------------------------------------------------------------

class StoryPage(BaseModel):
    page_number: int
    text: str
    illustration_url: Optional[str] = None
    audio_url: Optional[str] = None


# ---------------------------------------------------------------------------
# Story
# ---------------------------------------------------------------------------

class Story(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    title: str
    theme_tags: list[str] = Field(default_factory=list)
    pages: list[StoryPage] = Field(default_factory=list)
    duration_seconds: int = 240  # approx 4 minutes
    is_curated: bool = False
    is_ai_generated: bool = False
    created_for_child_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {"populate_by_name": True}


# ---------------------------------------------------------------------------
# Story Session
# ---------------------------------------------------------------------------

class StorySession(BaseModel):
    id: Optional[str] = Field(default=None, alias="_id")
    child_profile_id: str
    story_id: str
    started_at: datetime = Field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    voice_used: VoiceUsed = VoiceUsed.ai

    model_config = {"populate_by_name": True}
