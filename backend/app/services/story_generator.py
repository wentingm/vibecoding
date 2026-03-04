"""StoryGenerator service – wraps OpenAI to produce structured bedtime stories."""

import json
import re
from typing import Any

from openai import AsyncOpenAI

from app.core.config import settings

# System prompt shared across all story generation calls
_SYSTEM_PROMPT = (
    "You are a gentle bedtime story writer for children ages 3-7. "
    "Write safe, calming, age-appropriate stories with simple vocabulary "
    "and positive endings. No violence, no scary themes, no adult content."
)

# User prompt template
_USER_PROMPT_TEMPLATE = (
    "Write a bedtime story for {child_name} about {themes}. "
    "The story should have 5 pages, each with 2-3 short sentences. "
    "Format as JSON with fields: title, pages (array of {{page_number, text}})."
)


class StoryGenerator:
    """Async service that calls GPT-4o-mini and returns a structured story dict."""

    def __init__(self) -> None:
        self._client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def generate_story(
        self,
        child_name: str,
        themes: list[str],
        profile_id: str,
    ) -> dict[str, Any]:
        """Generate a bedtime story and return it as a structured dict.

        Returns a dict with the shape::

            {
                "title": str,
                "pages": [
                    {"page_number": int, "text": str},
                    ...
                ]
            }

        Raises ``ValueError`` if the model response cannot be parsed as JSON.
        """
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

        # Strip markdown code fences if the model wraps the JSON
        raw_content = re.sub(r"^```(?:json)?\s*", "", raw_content)
        raw_content = re.sub(r"\s*```$", "", raw_content)

        try:
            story_data: dict = json.loads(raw_content)
        except json.JSONDecodeError as exc:
            raise ValueError(
                f"OpenAI returned non-JSON content: {raw_content[:200]}"
            ) from exc

        # Normalise – ensure required keys exist
        if "title" not in story_data:
            story_data["title"] = f"{child_name}'s Bedtime Adventure"
        if "pages" not in story_data or not isinstance(story_data["pages"], list):
            raise ValueError("OpenAI response is missing 'pages' array.")

        # Ensure page_number is present on every page
        for idx, page in enumerate(story_data["pages"], start=1):
            if "page_number" not in page:
                page["page_number"] = idx

        return story_data
