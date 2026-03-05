"""Seed script – inserts 5 curated bedtime stories into MongoDB.

Run with the venv activated from the `backend/` directory:

    python seed_stories.py
"""

import asyncio
from datetime import datetime

import motor.motor_asyncio

# ---------------------------------------------------------------------------
# Configuration – mirrors app/core/config.py defaults / .env values
# ---------------------------------------------------------------------------
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
DATABASE_NAME = os.getenv("DATABASE_NAME", "bedtime_storyteller")

# ---------------------------------------------------------------------------
# Story data
# ---------------------------------------------------------------------------

CURATED_STORIES = [
    # ------------------------------------------------------------------
    # 1. The Dragon Who Couldn't Fly
    # ------------------------------------------------------------------
    {
        "title": "The Dragon Who Couldn't Fly",
        "theme_tags": ["dragon", "adventure", "friendship"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 240,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "In a cozy mountain valley lived a small dragon named Ember. "
                    "Ember had bright orange scales and a warm, glowing tail. "
                    "But no matter how hard he tried, Ember could not fly like the other dragons."
                ),
                "illustration_url": "illustrations/dragon_1.png",
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "Every morning Ember would climb to the top of the big round hill "
                    "and flap his wings as fast as he could. "
                    "He would lift just a tiny bit off the ground, then land gently in the soft grass."
                ),
                "illustration_url": "illustrations/dragon_2.png",
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "One day a small bluebird named Skye landed beside him. "
                    "'Why do you look so sad, Ember?' she asked. "
                    "'I cannot fly,' Ember sighed, 'and I feel left out.'"
                ),
                "illustration_url": "illustrations/dragon_3.png",
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "Skye smiled and taught Ember to tilt his wings like a kite in the breeze. "
                    "Ember tried once, twice, and on the third try he soared high above the valley! "
                    "He laughed with joy as the cool wind tickled his scales."
                ),
                "illustration_url": "illustrations/dragon_4.png",
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "That evening Ember and Skye sat together on a cloud and watched the stars appear. "
                    "'Thank you for being my friend,' said Ember. "
                    "Skye chirped happily, and the two friends fell asleep under the gentle moonlight."
                ),
                "illustration_url": "illustrations/dragon_5.png",
                "audio_url": None,
            },
        ],
    },

    # ------------------------------------------------------------------
    # 2. Olivia and the Moonbeam Fairy
    # ------------------------------------------------------------------
    {
        "title": "Olivia and the Moonbeam Fairy",
        "theme_tags": ["fairy", "moon", "magic"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 240,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "One quiet night, Olivia could not fall asleep. "
                    "She climbed out of bed and looked out her window at the big, bright moon. "
                    "A tiny sparkle of light drifted through the window and landed on her pillow."
                ),
                "illustration_url": "illustrations/fairy_1.png",
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "The sparkle grew into a tiny fairy no bigger than a thumb. "
                    "She had silver wings and a dress made of moonbeams. "
                    "'Hello, Olivia,' the fairy whispered. 'My name is Luna.'"
                ),
                "illustration_url": "illustrations/fairy_2.png",
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "Luna sprinkled a pinch of moon-dust above Olivia's head. "
                    "Suddenly Olivia felt light as a feather, and together they floated up through the window. "
                    "The whole town below looked like a tiny glittering toy."
                ),
                "illustration_url": "illustrations/fairy_3.png",
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "They danced among the silver clouds and counted the twinkling stars. "
                    "Luna sang a soft lullaby that sounded like wind chimes. "
                    "Olivia's eyes began to feel warm and heavy."
                ),
                "illustration_url": "illustrations/fairy_4.png",
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "Luna carried Olivia gently back to her cosy bed and tucked her in. "
                    "'Sweet dreams,' Luna whispered, and kissed her on the nose. "
                    "Olivia smiled, closed her eyes, and drifted into the most wonderful dream."
                ),
                "illustration_url": "illustrations/fairy_5.png",
                "audio_url": None,
            },
        ],
    },

    # ------------------------------------------------------------------
    # 3. Lucas and the Sleepy Stars
    # ------------------------------------------------------------------
    {
        "title": "Lucas and the Sleepy Stars",
        "theme_tags": ["space", "stars", "sleep"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 240,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "Lucas loved looking at the stars from his bedroom window. "
                    "One night he noticed that one star was blinking slower and slower. "
                    "'That star looks tired,' he said to himself."
                ),
                "illustration_url": "illustrations/space_1.png",
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "A friendly rocket with soft round windows appeared outside. "
                    "Its pilot, a small robot named Cosmo, waved at Lucas. "
                    "'Would you like to help me put the stars to sleep?' Cosmo asked."
                ),
                "illustration_url": "illustrations/space_2.png",
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "Lucas put on his cosy pajama spacesuit and they flew up through the dark sky. "
                    "Each star they visited was yawning and rubbing its eyes. "
                    "Lucas sang each one a quiet goodnight song."
                ),
                "illustration_url": "illustrations/space_3.png",
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "One by one the stars dimmed to a soft sleepy glow. "
                    "The whole sky turned into a gentle dark-blue blanket. "
                    "Lucas felt very proud of his important job."
                ),
                "illustration_url": "illustrations/space_4.png",
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "Cosmo flew Lucas home just as the last star blinked off. "
                    "'You are the best star-napper in the galaxy,' Cosmo said with a beep. "
                    "Lucas climbed into bed, pulled his blanket tight, and was asleep before his head hit the pillow."
                ),
                "illustration_url": "illustrations/space_5.png",
                "audio_url": None,
            },
        ],
    },

    # ------------------------------------------------------------------
    # 4. The Friendly Forest Animals
    # ------------------------------------------------------------------
    {
        "title": "The Friendly Forest Animals",
        "theme_tags": ["animals", "forest", "friendship"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 240,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "Deep in the Whispering Forest, the animals were getting ready for bed. "
                    "The fireflies switched on their tiny lights, and the crickets began to play a lullaby. "
                    "Everyone was tired after a long day of playing."
                ),
                "illustration_url": "illustrations/forest_1.png",
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "But little Pip the hedgehog could not find a cosy spot to sleep. "
                    "His usual pile of leaves had blown away in the evening breeze. "
                    "He sat on a log and let out a small, sad sigh."
                ),
                "illustration_url": "illustrations/forest_2.png",
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "Mama Rabbit hopped over and offered Pip a soft spot in her burrow. "
                    "Squirrel brought a pile of warm acorn-leaf blankets. "
                    "Even the old owl brought a feather pillow from his nest up in the oak tree."
                ),
                "illustration_url": "illustrations/forest_3.png",
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "Pip curled up into a cosy little ball surrounded by his friends. "
                    "He felt so warm and so happy that a big smile spread across his face. "
                    "'Thank you all,' he whispered."
                ),
                "illustration_url": "illustrations/forest_4.png",
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "The forest grew quiet as all the animals drifted off to sleep. "
                    "The moon peered through the leaves and smiled down at them. "
                    "In the Whispering Forest, no one ever had to sleep alone."
                ),
                "illustration_url": "illustrations/forest_5.png",
                "audio_url": None,
            },
        ],
    },

    # ------------------------------------------------------------------
    # 5. Lucas, Olivia and the Husky's Magic Trail
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia and the Husky's Magic Trail",
        "theme_tags": ["adventure", "siblings", "animals", "magic"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 300,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "One snowy evening, Lucas and Olivia were playing in the backyard "
                    "when they heard a soft howl from the woods. "
                    "Out of the trees trotted a beautiful white husky with bright blue eyes and a fluffy tail that wagged like a flag."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "The husky nudged Lucas's hand with his cold nose, then looked back at the forest. "
                    "'I think he wants us to follow him!' whispered Olivia, her eyes wide. "
                    "Lucas took his little sister's hand and together they stepped into the shimmering, snow-covered trees."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "Wherever the husky's paws touched the snow, tiny golden stars appeared. "
                    "The trail of stars wound through the forest like a glowing river. "
                    "Lucas and Olivia followed, laughing as snowflakes tickled their noses."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "The trail led to a cosy hollow tree filled with soft moss and warm light. "
                    "Inside sat a family of sleeping foxes, a snoozing owl, and three tiny rabbits all curled up together. "
                    "'It's the Dreamtime Den,' Olivia gasped, 'where all the forest animals sleep!'"
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "The husky curled up in the middle of the den and let out a long, happy yawn. "
                    "Lucas and Olivia snuggled beside him, warm and safe. "
                    "The golden stars drifted up through the branches and became the very stars in the sky above. "
                    "And just like that, the two siblings closed their eyes and dreamed of snowy trails and magic paws."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
        ],
    },

    # ------------------------------------------------------------------
    # 6. The Little Ocean Explorer
    # ------------------------------------------------------------------
    {
        "title": "The Little Ocean Explorer",
        "theme_tags": ["ocean", "adventure", "animals"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 240,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "Marina was a little sea turtle who loved to explore the ocean. "
                    "Every day she swam a little farther from her coral home. "
                    "Today she had found something she had never seen before – a glowing cave."
                ),
                "illustration_url": "illustrations/ocean_1.png",
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "Inside the cave, thousands of tiny blue jellyfish floated like lanterns. "
                    "They lit up the whole cave with a soft, dreamy glow. "
                    "Marina swam slowly among them, her eyes wide with wonder."
                ),
                "illustration_url": "illustrations/ocean_2.png",
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "A friendly dolphin named Delphi appeared at the cave entrance. "
                    "'This is the Sleepy Lantern Cave,' Delphi said. "
                    "'Every night the jellyfish glow to help ocean babies fall asleep.'"
                ),
                "illustration_url": "illustrations/ocean_3.png",
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "Marina listened to the soft bubbling sounds of the sea around her. "
                    "The gentle blue light made her feel peaceful and very, very sleepy. "
                    "She rested her head on a soft bed of sea-grass."
                ),
                "illustration_url": "illustrations/ocean_4.png",
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "Delphi tucked a piece of soft kelp around Marina like a blanket. "
                    "'Goodnight, little explorer,' Delphi sang in a low, gentle hum. "
                    "Marina closed her eyes and dreamed of all the wonders she would discover tomorrow."
                ),
                "illustration_url": "illustrations/ocean_5.png",
                "audio_url": None,
            },
        ],
    },
]


# ---------------------------------------------------------------------------
# Seeding logic
# ---------------------------------------------------------------------------

async def seed() -> None:
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGODB_URL)
    db = client[DATABASE_NAME]
    collection = db["stories"]

    inserted = 0
    skipped = 0

    for story in CURATED_STORIES:
        existing = await collection.find_one(
            {"title": story["title"], "is_curated": True}
        )
        if existing:
            print(f"  SKIP  '{story['title']}' (already exists)")
            skipped += 1
            continue

        result = await collection.insert_one(story)
        print(f"  INSERT '{story['title']}' → {result.inserted_id}")
        inserted += 1

    print(f"\nDone. {inserted} inserted, {skipped} skipped.")
    client.close()


if __name__ == "__main__":
    asyncio.run(seed())
