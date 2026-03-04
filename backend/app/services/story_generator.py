"""StoryGenerator service – wraps OpenAI to produce structured bedtime stories with TTS audio."""

import asyncio
import json
import pathlib
import re
import uuid
from typing import Any

import httpx
from openai import AsyncOpenAI

from app.core.config import settings

AUDIO_DIR = pathlib.Path(__file__).parent.parent.parent / "static" / "audio"
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

_SYSTEM_PROMPT = (
    "You are a gentle bedtime story writer for children ages 3-7. "
    "Write safe, calming, age-appropriate stories with simple vocabulary "
    "and positive endings. No violence, no scary themes, no adult content."
)

_USER_PROMPT_TEMPLATE = (
    "Write a bedtime story for {child_name} about {themes}. "
    "The story should have 5 pages, each with 2-3 short sentences. "
    "Format as JSON with fields: title, pages (array of {{page_number, text}})."
)

# Theme → (emoji, bg_color)
_THEME_MAP: dict[str, tuple[str, str]] = {
    "dragon":     ("🐉", "#3D1C6E"),
    "fairy":      ("🧚", "#7B3FA0"),
    "space":      ("🚀", "#0D1B4B"),
    "animals":    ("🦁", "#7B5E3A"),
    "ocean":      ("🐋", "#0B3D6E"),
    "princess":   ("👸", "#8E3A6E"),
    "robot":      ("🤖", "#2D4A6E"),
    "magic":      ("✨", "#4B2D8E"),
    "adventure":  ("🗺️", "#3A5E3A"),
    "friendship": ("🌈", "#3A6E5B"),
    "forest":     ("🌲", "#2D5A2D"),
    "castle":     ("🏰", "#5A3A7B"),
    "stars":      ("⭐", "#1A1A4B"),
    "rainbow":    ("🌈", "#5B3A8E"),
    "unicorn":    ("🦄", "#7B3A8E"),
}
_DEFAULT_EMOJI = "📖"
_DEFAULT_BG = "#2D1B69"


def _pick_emoji_and_color(themes: list[str]) -> tuple[str, str]:
    for theme in themes:
        key = theme.lower()
        if key in _THEME_MAP:
            return _THEME_MAP[key]
    return _DEFAULT_EMOJI, _DEFAULT_BG


class StoryGenerator:
    def __init__(self) -> None:
        self._client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def _generate_audio(self, text: str, filename: str) -> str:
        """Generate TTS audio using ElevenLabs (if configured) or OpenAI nova."""
        filepath = AUDIO_DIR / filename

        if settings.ELEVENLABS_API_KEY and settings.ELEVENLABS_VOICE_ID:
            try:
                url = f"https://api.elevenlabs.io/v1/text-to-speech/{settings.ELEVENLABS_VOICE_ID}"
                headers = {
                    "xi-api-key": settings.ELEVENLABS_API_KEY,
                    "Content-Type": "application/json",
                }
                payload = {
                    "text": text,
                    "model_id": "eleven_multilingual_v2",
                    "voice_settings": {"stability": 0.75, "similarity_boost": 0.80},
                }
                async with httpx.AsyncClient(timeout=30) as client:
                    resp = await client.post(url, headers=headers, json=payload)
                    resp.raise_for_status()
                filepath.write_bytes(resp.content)
                return f"{settings.BASE_URL}/static/audio/{filename}"
            except Exception as e:
                print(f"ElevenLabs failed, falling back to OpenAI TTS: {e}")

        # Fallback: OpenAI nova voice
        response = await self._client.audio.speech.create(
            model="tts-1",
            voice="nova",
            input=text,
        )
        filepath.write_bytes(response.content)
        return f"{settings.BASE_URL}/static/audio/{filename}"

    async def generate_story(
        self,
        child_name: str,
        themes: list[str],
        profile_id: str,
    ) -> dict[str, Any]:
        themes_str = ", ".join(themes)
        user_prompt = _USER_PROMPT_TEMPLATE.format(
            child_name=child_name,
            themes=themes_str,
        )

        response = await self._client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": _SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.8,
            max_tokens=1500,
        )

        raw_content: str = response.choices[0].message.content.strip()
        raw_content = re.sub(r"^```(?:json)?\s*", "", raw_content)
        raw_content = re.sub(r"\s*```$", "", raw_content)

        try:
            story_data: dict = json.loads(raw_content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"OpenAI returned non-JSON content: {raw_content[:200]}"
            ) from exc

        if "title" not in story_data:
            story_data["title"] = f"{child_name}'s Bedtime Adventure"
        if "pages" not in story_data or not isinstance(story_data["pages"], list):
            raise ValueError("OpenAI response is missing 'pages' array.")

        for idx, page in enumerate(story_data["pages"], start=1):
            if "page_number" not in page:
                page["page_number"] = idx

        # Generate TTS audio for all pages in parallel
        story_slug = str(uuid.uuid4())[:8]
        emoji, bg_color = _pick_emoji_and_color(themes)

        audio_tasks = [
            self._generate_audio(
                page["text"],
                f"{story_slug}_page_{page['page_number']}.mp3",
            )
            for page in story_data["pages"]
        ]
        audio_urls = await asyncio.gather(*audio_tasks, return_exceptions=True)

        for page, audio_url in zip(story_data["pages"], audio_urls):
            page["audio_url"] = audio_url if isinstance(audio_url, str) else None
            page["emoji"] = emoji
            page["bg_color"] = bg_color

        return story_data
