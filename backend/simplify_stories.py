"""Simplify all curated story text for 5-year-old children, then re-enrich audio."""

import asyncio
import os
import pathlib

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from openai import AsyncOpenAI

load_dotenv(override=True)

MONGO_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DB_NAME   = os.getenv("DATABASE_NAME", "bedtime_storyteller")
client    = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

AUDIO_DIR = pathlib.Path("static/audio")

SYSTEM_PROMPT = """You are a children's book editor who rewrites story pages for 5-year-old children.

Rules:
- Use only very simple, short words (no more than 2 syllables when possible)
- Keep sentences short — maximum 15 words each
- Use 2-3 sentences per page
- Write warmly and playfully
- Keep the same characters and same story event — just make the language simpler
- Do NOT add new plot points or change what happens
- Do NOT use words like: shimmering, galloped, trembled, glimpsed, proclaimed, elegant, murmured
- DO use words like: ran, bright, smiled, said, happy, cozy, soft, warm, big, little
- Keep dialogue natural and simple, like a child would say it
- Output ONLY the rewritten page text, nothing else"""


async def simplify_page(text: str) -> str:
    resp = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"Rewrite this story page for a 5-year-old:\n\n{text}"},
        ],
        temperature=0.4,
        max_tokens=200,
    )
    return resp.choices[0].message.content.strip()


def delete_audio(story_id: str, page_number: int):
    """Remove cached mp3 so enrich_stories will regenerate it."""
    path = AUDIO_DIR / f"{story_id}_page_{page_number}.mp3"
    if path.exists():
        path.unlink()


async def main():
    mongo = AsyncIOMotorClient(MONGO_URL)
    db = mongo[DB_NAME]

    stories = await db["stories"].find({"is_curated": True}).to_list(length=100)
    print(f"Simplifying {len(stories)} stories...\n")

    for story in stories:
        title = story["title"]
        sid   = str(story["_id"])
        print(f"📖 {title}")

        updated_pages = []
        for page in story["pages"]:
            n = page["page_number"]
            original = page["text"]
            simplified = await simplify_page(original)
            print(f"  Page {n}: {simplified[:60]}...")

            # Delete old audio so enrich regenerates it
            delete_audio(sid, n)

            updated_pages.append({**page, "text": simplified, "audio_url": None})

        await db["stories"].update_one(
            {"_id": story["_id"]},
            {"$set": {"pages": updated_pages}},
        )
        print(f"  ✓ saved\n")

    mongo.close()
    print("✅ All stories simplified! Now run enrich_stories.py to regenerate audio.")


asyncio.run(main())
