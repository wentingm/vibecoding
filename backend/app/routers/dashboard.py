"""Parental dashboard routes – require auth AND a valid parent passcode."""

from typing import Annotated

from bson import ObjectId
from fastapi import APIRouter, Depends, Header, HTTPException, status
from motor.motor_asyncio import AsyncIOMotorDatabase
from pydantic import BaseModel

from app.core.deps import get_current_user, get_db

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


# ---------------------------------------------------------------------------
# Response models
# ---------------------------------------------------------------------------

class ChildSummary(BaseModel):
    child_profile_id: str
    child_name: str
    stories_played: int
    total_duration_seconds: int
    last_active: str | None  # ISO datetime string or None


class DashboardResponse(BaseModel):
    family_name: str
    children: list[ChildSummary]


# ---------------------------------------------------------------------------
# Passcode verification helper
# ---------------------------------------------------------------------------

async def _verify_passcode(
    current_user: dict,
    x_parent_passcode: str,
) -> None:
    """Raise HTTP 403 when the supplied passcode does not match the stored one."""
    stored = current_user.get("parent_passcode", "")
    if x_parent_passcode != stored:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid parent passcode.",
        )


# ---------------------------------------------------------------------------
# GET /dashboard
# ---------------------------------------------------------------------------

@router.get("", response_model=DashboardResponse)
async def get_dashboard(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
    x_parent_passcode: Annotated[str, Header(alias="X-Parent-Passcode")] = "",
) -> DashboardResponse:
    """Return a per-child activity summary for the current family.

    Requires the ``X-Parent-Passcode`` header to match the stored 4-digit PIN.
    """
    await _verify_passcode(current_user, x_parent_passcode)

    # Fetch all non-deleted child profiles
    cursor = db["child_profiles"].find(
        {"user_id": current_user["_id"], "is_deleted": False}
    )
    profiles = await cursor.to_list(length=10)

    children: list[ChildSummary] = []
    for profile in profiles:
        profile_id = str(profile["_id"])

        # Aggregate session stats for this child
        pipeline = [
            {"$match": {"child_profile_id": profile_id}},
            {
                "$group": {
                    "_id": None,
                    "count": {"$sum": 1},
                    "total_duration": {"$sum": {"$ifNull": ["$duration_seconds", 0]}},
                    "last_active": {"$max": "$started_at"},
                }
            },
        ]
        agg_result = await db["story_sessions"].aggregate(pipeline).to_list(length=1)

        if agg_result:
            stats = agg_result[0]
            stories_played = stats["count"]
            total_duration = stats["total_duration"]
            last_active_dt = stats.get("last_active")
            last_active = last_active_dt.isoformat() if last_active_dt else None
        else:
            stories_played = 0
            total_duration = 0
            last_active = None

        children.append(
            ChildSummary(
                child_profile_id=profile_id,
                child_name=profile["name"],
                stories_played=stories_played,
                total_duration_seconds=total_duration,
                last_active=last_active,
            )
        )

    return DashboardResponse(
        family_name=current_user["family_name"],
        children=children,
    )


# ---------------------------------------------------------------------------
# GET /dashboard/{child_id}/sessions
# ---------------------------------------------------------------------------

class SessionHistoryItem(BaseModel):
    session_id: str
    story_id: str
    started_at: str
    completed_at: str | None
    duration_seconds: int | None
    voice_used: str


@router.get("/{child_id}/sessions", response_model=list[SessionHistoryItem])
async def get_child_sessions(
    child_id: str,
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
    x_parent_passcode: Annotated[str, Header(alias="X-Parent-Passcode")] = "",
) -> list[SessionHistoryItem]:
    """Return the full session history for a specific child.

    Requires the ``X-Parent-Passcode`` header.
    """
    await _verify_passcode(current_user, x_parent_passcode)

    # Verify the child belongs to the current user
    try:
        child_oid = ObjectId(child_id)
    except Exception:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Child profile not found.")

    profile = await db["child_profiles"].find_one(
        {"_id": child_oid, "user_id": current_user["_id"], "is_deleted": False}
    )
    if profile is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Child profile not found.")

    cursor = (
        db["story_sessions"]
        .find({"child_profile_id": child_id})
        .sort("started_at", -1)
        .limit(100)
    )
    sessions = await cursor.to_list(length=100)

    result: list[SessionHistoryItem] = []
    for s in sessions:
        completed_at = s.get("completed_at")
        result.append(
            SessionHistoryItem(
                session_id=str(s["_id"]),
                story_id=s["story_id"],
                started_at=s["started_at"].isoformat(),
                completed_at=completed_at.isoformat() if completed_at else None,
                duration_seconds=s.get("duration_seconds"),
                voice_used=s.get("voice_used", "ai"),
            )
        )
    return result
