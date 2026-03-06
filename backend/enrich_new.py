"""Enrich only new stories (missing audio) + regenerate Paw Patrol images."""

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

    SHOW_STYLES = {
        "peppa":      "bright bold flat cartoon style, cheerful pink pig family, green hills, muddy puddles,",
        "bluey":      "bright Australian cartoon style, blue and orange heeler puppy family, warm colourful backyard,",
        "cocomelon":  "soft rounded 3D cartoon style, bright primary colours, cheerful toddler characters,",
        "tinga":      "vibrant African folk-art style, bold flat colours, decorative patterns, colourful animals,",
        "helper":     "bright bold cartoon style, friendly smiling colourful vehicles, clean roads and buildings,",
        "octonaut":   "deep ocean adventure cartoon style, glowing underwater scenes, cute animal explorers in wetsuits,",
        "paw patrol": "bright rescue adventure cartoon style, colourful puppy heroes in uniforms, Adventure Bay scenery,",
    }
    style_hint = ""
    title_lower = title.lower()
    for key, style in SHOW_STYLES.items():
        if key in title_lower:
            style_hint = style
            break

    base_style = style_hint if style_hint else "gentle soft watercolor style, warm pastel colors, dreamy and calming,"

    prompts = [
        (
            f"A children's book illustration in {base_style} "
            f"suitable for bedtime, ages 3-7. "
            f"Scene: {text[:180]}. No text or letters in the image."
        ),
        (
            f"A children's book scene in {base_style} "
            f"from the story '{title}'. Cosy and magical bedtime atmosphere. "
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


async def enrich_story(db, story: dict, regen_images: bool = False):
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

        # Regen images if requested (e.g. Paw Patrol fix)
        if regen_images:
            img_path = IMAGE_DIR / image_filename
            if img_path.exists():
                img_path.unlink()

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

    all_stories = await db["stories"].find({"is_curated": True}).to_list(length=100)

    # Process stories missing audio
    need_audio = [s for s in all_stories if not any(p.get("audio_url") for p in s["pages"])]
    print(f"Found {len(need_audio)} stories needing audio")
    for story in need_audio:
        await enrich_story(db, story)

    # Re-enrich Paw Patrol with new image style
    from bson import ObjectId
    paw_story = await db["stories"].find_one({"_id": ObjectId("69a8d79344761981ea4d1e6f")})
    if paw_story:
        print(f"\n🐾 Re-generating Paw Patrol images...")
        await enrich_story(db, paw_story, regen_images=True)

    mongo.close()
    print("\n✅ Done!")


asyncio.run(main())
