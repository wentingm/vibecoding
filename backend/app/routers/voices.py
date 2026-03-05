"""Voice upload and ElevenLabs voice cloning routes."""

import pathlib
from typing import Annotated

import httpx
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from motor.motor_asyncio import AsyncIOMotorDatabase

from app.core.config import settings
from app.core.deps import get_current_user, get_db

AUDIO_DIR = pathlib.Path("static/audio")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

router = APIRouter(prefix="/voices", tags=["voices"])


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_voice(
    current_user: Annotated[dict, Depends(get_current_user)],
    db: Annotated[AsyncIOMotorDatabase, Depends(get_db)],
    label: str = Form(..., description="'Mom' or 'Dad'"),
    file: UploadFile = File(...),
):
    """Upload a voice recording, clone it via ElevenLabs, save voice_id to user profile."""
    if not settings.ELEVENLABS_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ElevenLabs API key not configured.",
        )

    audio_data = await file.read()
    if len(audio_data) < 10_000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Audio file too small. Please upload at least 30 seconds of audio.",
        )

    # Upload to ElevenLabs Voice Clone API
    try:
        async with httpx.AsyncClient(timeout=60) as client:
            resp = await client.post(
                "https://api.elevenlabs.io/v1/voices/add",
                headers={"xi-api-key": settings.ELEVENLABS_API_KEY},
                data={"name": f"{label} - Bedtime Stories"},
                files={"files": (file.filename or "voice.m4a", audio_data, file.content_type or "audio/m4a")},
            )
            resp.raise_for_status()
            voice_id = resp.json()["voice_id"]
    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"ElevenLabs error: {e.response.text}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Voice cloning failed: {e}",
        )

    # Save voice_id to user record
    field = "mom_voice_id" if label.lower() == "mom" else "dad_voice_id"
    await db["users"].update_one(
        {"_id": current_user["_id"]},
        {"$set": {field: voice_id}},
    )

    return {"voice_id": voice_id, "label": label, "message": "Voice cloned successfully!"}


@router.get("/my-voices")
async def get_my_voices(
    current_user: Annotated[dict, Depends(get_current_user)],
):
    """Return the saved voice IDs for the current user."""
    return {
        "mom_voice_id": current_user.get("mom_voice_id"),
        "dad_voice_id": current_user.get("dad_voice_id"),
    }


@router.get("/greeting")
async def get_greeting(
    name: str,
    time_of_day: str = "evening",
):
    """Generate and cache a personalized greeting in the cloned voice."""
    if not settings.ELEVENLABS_API_KEY or not settings.ELEVENLABS_VOICE_ID:
        raise HTTPException(status_code=503, detail="ElevenLabs not configured.")

    greeting_text = f"Good {time_of_day}, {name}! Ready for a bedtime story?"
    safe_name = "".join(c for c in name.lower() if c.isalnum())
    filename = f"greeting_{safe_name}_{time_of_day}.mp3"
    path = AUDIO_DIR / filename

    # Serve cached file if it exists
    if path.exists():
        return {"url": f"{settings.BASE_URL}/static/audio/{filename}"}

    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{settings.ELEVENLABS_VOICE_ID}"
        payload = {
            "text": greeting_text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {"stability": 0.75, "similarity_boost": 0.80},
        }
        async with httpx.AsyncClient(timeout=30) as client:
            resp = await client.post(
                url,
                headers={"xi-api-key": settings.ELEVENLABS_API_KEY, "Content-Type": "application/json"},
                json=payload,
            )
            resp.raise_for_status()
        path.write_bytes(resp.content)
        return {"url": f"{settings.BASE_URL}/static/audio/{filename}"}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Greeting generation failed: {e}")
