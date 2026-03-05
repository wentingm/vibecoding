"""Enrich curated stories with TTS audio and DALL-E illustrations."""

import asyncio
import os
import pathlib

import httpx
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from openai import AsyncOpenAI

load_dotenv(override=True)

MONGO_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME = os.getenv("DATABASE_NAME", "bedtime_storyteller")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")
ELEVENLABS_KEY = os.getenv("ELEVENLABS_API_KEY", "")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID", "")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

AUDIO_DIR = pathlib.Path("static/audio")
IMAGE_DIR = pathlib.Path("static/images")
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
IMAGE_DIR.mkdir(parents=True, exist_ok=True)

THEME_MAP = {
    "dragon":     ("🐉", "#3D1C6E"),
    "fairy":      ("🧚", "#7B3FA0"),
    "space":      ("🚀", "#0D1B4B"),
    "animals":    ("🦁", "#7B5E3A"),
    "ocean":      ("🐋", "#0B3D6E"),
    "forest":     ("🌲", "#2D5A2D"),
    "stars":      ("⭐", "#1A1A4B"),
    "princess":   ("👸", "#8E3A6E"),
}

client = AsyncOpenAI(api_key=OPENAI_KEY)


def pick_emoji_color(themes: list[str]) -> tuple[str, str]:
    for theme in themes:
        for key, val in THEME_MAP.items():
            if key in theme.lower():
                return val
    return ("📖", "#2D1B69")


async def generate_tts(text: str, filename: str) -> str:
    path = AUDIO_DIR / filename
    # Don't use cache — always regenerate so voice changes take effect
    if ELEVENLABS_KEY and ELEVENLABS_VOICE_ID:
        try:
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
            headers = {"xi-api-key": ELEVENLABS_KEY, "Content-Type": "application/json"}
            payload = {
                "text": text,
                "model_id": "eleven_multilingual_v2",
                "voice_settings": {"stability": 0.75, "similarity_boost": 0.80},
            }
            async with httpx.AsyncClient(timeout=30) as http:
                resp = await http.post(url, headers=headers, json=payload)
                resp.raise_for_status()
            path.write_bytes(resp.content)
            print(f"    ElevenLabs audio: {filename}")
            return f"{BASE_URL}/static/audio/{filename}"
        except Exception as e:
            print(f"    ElevenLabs failed ({e}), falling back to OpenAI")
    response = await client.audio.speech.create(model="tts-1-hd", voice="onyx", input=text)
    path.write_bytes(response.content)
    return f"{BASE_URL}/static/audio/{filename}"


async def generate_image(text: str, title: str, filename: str) -> str:
    path = IMAGE_DIR / filename
    if path.exists():
        print(f"    image cached: {filename}")
        return f"{BASE_URL}/static/images/{filename}"

    prompts = [
        (
            f"A gentle children's book illustration in soft watercolor style, "
            f"warm pastel colors, dreamy and calming, suitable for bedtime, ages 3-7. "
            f"Scene: {text[:180]}. No text or letters in the image."
        ),
        (
            f"A soft watercolor children's book scene from the story '{title}'. "
            f"Warm pastel colors, cosy and magical, bedtime atmosphere. "
            f"No text or letters in the image."
        ),
    ]

    for prompt in prompts:
        try:
            response = await client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            image_url = response.data[0].url
            async with httpx.AsyncClient(timeout=30) as http:
                img_resp = await http.get(image_url)
            path.write_bytes(img_resp.content)
            return f"{BASE_URL}/static/images/{filename}"
        except Exception as e:
            print(f"    image prompt failed ({e}), trying fallback...")
            continue

    print(f"    ⚠️  all image prompts failed, skipping image")
    return ""


async def enrich_story(db, story: dict):
    title = story["title"]
    slug = str(story["_id"])
    themes = story.get("theme_tags", [])
    emoji, bg_color = pick_emoji_color(themes)

    print(f"\n📖 {title}")

    updated_pages = []
    for page in story["pages"]:
        n = page["page_number"]
        print(f"  Page {n}...")

        audio_filename = f"{slug}_page_{n}.mp3"
        image_filename = f"{slug}_page_{n}.jpg"

        # Run TTS and image generation in parallel
        audio_url, image_url = await asyncio.gather(
            generate_tts(page["text"], audio_filename),
            generate_image(page["text"], title, image_filename),
        )
        print(f"    ✓ audio + image")

        updated_pages.append({
            **page,
            "audio_url": audio_url,
            "illustration_url": image_url,
            "emoji": emoji,
            "bg_color": bg_color,
        })

    await db["stories"].update_one(
        {"_id": story["_id"]},
        {"$set": {"pages": updated_pages}},
    )
    print(f"  ✓ saved to DB")


async def main():
    mongo = AsyncIOMotorClient(MONGO_URL)
    db = mongo[DB_NAME]

    stories = await db["stories"].find({"is_curated": True}).to_list(length=100)
    print(f"Found {len(stories)} curated stories to enrich")

    for story in stories:
        await enrich_story(db, story)

    mongo.close()
    print("\n✅ All stories enriched!")


asyncio.run(main())
