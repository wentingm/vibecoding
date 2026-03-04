"""Story routes: browse curated stories, AI generation, and session tracking."""

from datetime import datetime
from typing import Annotated, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, Query, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.deps import get_current_user, get_db
from app.schemas.story import (
    GenerateStoryRequest,
    StartSessionRequest,
    StoryPageResponse,
    StoryResponse,
    StorySessionResponse,
    UpdateSessionRequest,
)
from app.services.story_generator import StoryGenerator

router = APIRouter(prefix="/stories", tags=["stories"])

# Shared service instance (stateless, safe to re-use across requests)
_story_generator = StoryGenerator()


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _story_doc_to_response(doc: dict) -> StoryResponse:
    pages = [
        StoryPageResponse(
            page_number=p["page_number"],
            text=p["text"],
            illustration_url=p.get("illustration_url"),
            audio_url=p.get("audio_url"),
        )
        for p in doc.get("pages", [])
    ]
    return StoryResponse(
        id=str(doc["_id"]),
        title=doc["title"],
        theme_tags=doc.get("theme_tags", []),
        pages=pages,
        duration_seconds=doc.get("duration_seconds", 240),
        is_curated=doc.get("is_curated", False),
        is_ai_generated=doc.get("is_ai_generated", False),
        created_for_child_id=doc.get("created_for_child_id"),
        created_at=doc["created_at"],
    )


def _session_doc_to_response(doc: dict) -> StorySessionResponse:
    return StorySessionResponse(
        id=str(doc["_id"]),
        child_profile_id=doc["child_profile_id"],
        story_id=doc["story_id"],
        started_at=doc["started_at"],
        completed_at=doc.get("completed_at"),
        duration_seconds=doc.get("duration_seconds"),
        voice_used=doc.get("voice_used", "ai"),
    )


# ---------------------------------------------------------------------------
# GET /stories
# ---------------------------------------------------------------------------

@router.get("", response_model=list[StoryResponse])
async def list_stories(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
    themes: Optional[str] = Query(
        default=None,
        description="Comma-separated theme tags to filter by, e.g. 'dragon,fairy'",
    ),
) -> list[StoryResponse]:
    """List curated stories, optionally filtered by theme tags."""
    query: dict = {"is_curated": True}
    if themes:
        tag_list = [t.strip() for t in themes.split(",") if t.strip()]
        if tag_list:
            query["theme_tags"] = {"$in": tag_list}

    cursor = db["stories"].find(query).sort("created_at", -1).limit(50)
    docs = await cursor.to_list(length=50)
    return [_story_doc_to_response(d) for d in docs]


# ---------------------------------------------------------------------------
# GET /stories/{story_id}
# ---------------------------------------------------------------------------

@router.get("/{story_id}", response_model=StoryResponse)
async def get_story(
    story_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> StoryResponse:
    """Fetch a single story with all its pages."""
    try:
        oid = ObjectId(story_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found.")

    doc = await db["stories"].find_one({"_id": oid})
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found.")
    return _story_doc_to_response(doc)


# ---------------------------------------------------------------------------
# POST /stories/generate
# ---------------------------------------------------------------------------

@router.post("/generate", response_model=StoryResponse, status_code=status.HTTP_201_CREATED)
async def generate_story(
    payload: GenerateStoryRequest,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> StoryResponse:
    """Generate an AI-authored bedtime story using GPT-4o-mini and save it to the DB."""
    try:
        story_data = await _story_generator.generate_story(
            child_name=payload.child_name,
            themes=payload.themes,
            profile_id=payload.child_profile_id,
        )
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Story generation failed: {exc}",
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Unexpected error during story generation: {exc}",
        )

    pages = [
        {
            "page_number": p["page_number"],
            "text": p["text"],
            "illustration_url": None,
            "audio_url": None,
        }
        for p in story_data.get("pages", [])
    ]

    # Estimate duration: ~30 seconds per page
    duration_seconds = len(pages) * 30

    story_doc = {
        "title": story_data["title"],
        "theme_tags": payload.themes,
        "pages": pages,
        "duration_seconds": duration_seconds,
        "is_curated": False,
        "is_ai_generated": True,
        "created_for_child_id": payload.child_profile_id,
        "created_at": datetime.utcnow(),
    }

    result = await db["stories"].insert_one(story_doc)
    story_doc["_id"] = result.inserted_id
    return _story_doc_to_response(story_doc)


# ---------------------------------------------------------------------------
# POST /stories/sessions
# ---------------------------------------------------------------------------

@router.post("/sessions", response_model=StorySessionResponse, status_code=status.HTTP_201_CREATED)
async def start_session(
    payload: StartSessionRequest,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> StorySessionResponse:
    """Log the start of a story playback session."""
    # Verify the story exists
    try:
        story_oid = ObjectId(payload.story_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found.")

    story = await db["stories"].find_one({"_id": story_oid})
    if story is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Story not found.")

    session_doc = {
        "child_profile_id": payload.child_profile_id,
        "story_id": payload.story_id,
        "started_at": datetime.utcnow(),
        "completed_at": None,
        "duration_seconds": None,
        "voice_used": payload.voice_used.value,
    }
    result = await db["story_sessions"].insert_one(session_doc)
    session_doc["_id"] = result.inserted_id
    return _session_doc_to_response(session_doc)


# ---------------------------------------------------------------------------
# PUT /stories/sessions/{session_id}
# ---------------------------------------------------------------------------

@router.put("/sessions/{session_id}", response_model=StorySessionResponse)
async def update_session(
    session_id: str,
    payload: UpdateSessionRequest,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> StorySessionResponse:
    """Update a story session (e.g. mark as completed)."""
    try:
        oid = ObjectId(session_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")

    doc = await db["story_sessions"].find_one({"_id": oid})
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found.")

    updates = payload.model_dump(exclude_none=True)
    if updates:
        await db["story_sessions"].update_one({"_id": oid}, {"$set": updates})

    updated = await db["story_sessions"].find_one({"_id": oid})
    return _session_doc_to_response(updated)
