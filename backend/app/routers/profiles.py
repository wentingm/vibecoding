"""Child profile and voice profile routes."""

from datetime import datetime
from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.deps import get_current_user, get_db
from app.schemas.profile import (
    ChildProfileResponse,
    CreateChildProfileRequest,
    CreateVoiceProfileRequest,
    UpdateChildProfileRequest,
    VoiceProfileResponse,
)

router = APIRouter(prefix="/profiles", tags=["profiles"])

_MAX_CHILD_PROFILES = 4


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _profile_doc_to_response(doc: dict) -> ChildProfileResponse:
    return ChildProfileResponse(
        id=str(doc["_id"]),
        user_id=str(doc["user_id"]),
        name=doc["name"],
        avatar=doc["avatar"],
        age=doc["age"],
        allowed_themes=doc.get("allowed_themes", []),
        blocked_themes=doc.get("blocked_themes", []),
        story_intensity=doc.get("story_intensity", "calm"),
        sleep_timer_default=doc.get("sleep_timer_default", 20),
        created_at=doc["created_at"],
    )


def _voice_doc_to_response(doc: dict) -> VoiceProfileResponse:
    return VoiceProfileResponse(
        id=str(doc["_id"]),
        user_id=str(doc["user_id"]),
        child_profile_id=str(doc["child_profile_id"]),
        label=doc["label"],
        elevenlabs_voice_id=doc["elevenlabs_voice_id"],
        recording_url=doc.get("recording_url"),
        created_at=doc["created_at"],
    )


async def _get_profile_or_404(
    profile_id: str,
    user_id: str,
    db: AsyncIOMotorDatabase,
) -> dict:
    """Fetch a non-deleted child profile that belongs to *user_id*."""
    try:
        oid = ObjectId(profile_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found.")

    doc = await db["child_profiles"].find_one(
        {"_id": oid, "user_id": user_id, "is_deleted": False}
    )
    if doc is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Profile not found.")
    return doc


# ---------------------------------------------------------------------------
# GET /profiles
# ---------------------------------------------------------------------------

@router.get("", response_model=list[ChildProfileResponse])
async def list_profiles(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> list[ChildProfileResponse]:
    """List all non-deleted child profiles for the current user."""
    cursor = db["child_profiles"].find(
        {"user_id": current_user["_id"], "is_deleted": False}
    )
    docs = await cursor.to_list(length=_MAX_CHILD_PROFILES + 1)
    return [_profile_doc_to_response(d) for d in docs]


# ---------------------------------------------------------------------------
# POST /profiles
# ---------------------------------------------------------------------------

@router.post("", response_model=ChildProfileResponse, status_code=status.HTTP_201_CREATED)
async def create_profile(
    payload: CreateChildProfileRequest,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> ChildProfileResponse:
    """Create a new child profile (max 4 per family account)."""
    count = await db["child_profiles"].count_documents(
        {"user_id": current_user["_id"], "is_deleted": False}
    )
    if count >= _MAX_CHILD_PROFILES:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Maximum of {_MAX_CHILD_PROFILES} child profiles allowed per account.",
        )

    doc = {
        "user_id": current_user["_id"],
        "name": payload.name,
        "avatar": payload.avatar,
        "age": payload.age,
        "allowed_themes": payload.allowed_themes,
        "blocked_themes": payload.blocked_themes,
        "story_intensity": payload.story_intensity.value,
        "sleep_timer_default": payload.sleep_timer_default,
        "created_at": datetime.utcnow(),
        "is_deleted": False,
    }
    result = await db["child_profiles"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return _profile_doc_to_response(doc)


# ---------------------------------------------------------------------------
# PUT /profiles/{profile_id}
# ---------------------------------------------------------------------------

@router.put("/{profile_id}", response_model=ChildProfileResponse)
async def update_profile(
    profile_id: str,
    payload: UpdateChildProfileRequest,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> ChildProfileResponse:
    """Update fields on an existing child profile."""
    await _get_profile_or_404(profile_id, current_user["_id"], db)

    updates = payload.model_dump(exclude_none=True)
    if "story_intensity" in updates:
        updates["story_intensity"] = updates["story_intensity"].value

    if not updates:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No fields provided for update.",
        )

    await db["child_profiles"].update_one(
        {"_id": ObjectId(profile_id)},
        {"$set": updates},
    )

    updated = await db["child_profiles"].find_one({"_id": ObjectId(profile_id)})
    return _profile_doc_to_response(updated)


# ---------------------------------------------------------------------------
# DELETE /profiles/{profile_id}
# ---------------------------------------------------------------------------

@router.delete("/{profile_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_profile(
    profile_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> None:
    """Soft-delete a child profile."""
    await _get_profile_or_404(profile_id, current_user["_id"], db)
    await db["child_profiles"].update_one(
        {"_id": ObjectId(profile_id)},
        {"$set": {"is_deleted": True}},
    )


# ---------------------------------------------------------------------------
# GET /profiles/{profile_id}/voice
# ---------------------------------------------------------------------------

@router.get("/{profile_id}/voice", response_model=list[VoiceProfileResponse])
async def list_voice_profiles(
    profile_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> list[VoiceProfileResponse]:
    """List voice profiles attached to a specific child profile."""
    await _get_profile_or_404(profile_id, current_user["_id"], db)

    cursor = db["voice_profiles"].find(
        {"child_profile_id": profile_id, "user_id": current_user["_id"]}
    )
    docs = await cursor.to_list(length=20)
    return [_voice_doc_to_response(d) for d in docs]


# ---------------------------------------------------------------------------
# POST /profiles/{profile_id}/voice
# ---------------------------------------------------------------------------

@router.post(
    "/{profile_id}/voice",
    response_model=VoiceProfileResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_voice_profile(
    profile_id: str,
    payload: CreateVoiceProfileRequest,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
) -> VoiceProfileResponse:
    """Link an ElevenLabs voice ID to a child profile."""
    await _get_profile_or_404(profile_id, current_user["_id"], db)

    doc = {
        "user_id": current_user["_id"],
        "child_profile_id": profile_id,
        "label": payload.label,
        "elevenlabs_voice_id": payload.elevenlabs_voice_id,
        "recording_url": payload.recording_url,
        "created_at": datetime.utcnow(),
    }
    result = await db["voice_profiles"].insert_one(doc)
    doc["_id"] = result.inserted_id
    return _voice_doc_to_response(doc)
