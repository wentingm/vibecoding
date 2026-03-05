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
    # ------------------------------------------------------------------
    # 7. Lucas and Olivia's Deep Sea Adventure
    # ------------------------------------------------------------------
    {
        "title": "Lucas and Olivia's Deep Sea Adventure",
        "theme_tags": ["ocean", "adventure", "animals", "siblings"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 360,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "One morning Lucas and Olivia found a shimmering submarine at the end of their garden path. "
                    "It was small and round, with a porthole window and a friendly blinking light on top. "
                    "'Shall we go in?' whispered Olivia. Lucas grabbed her hand, and together they dove beneath the waves."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "The first friend they met was Bella the blue whale — the biggest, gentlest creature in all the sea. "
                    "Bella blew a huge, sparkling water spout that caught the sunlight like a rainbow. "
                    "'Hold on tight!' she rumbled softly, and the children laughed as bubbles swirled all around them."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "Next, Inky the octopus waved all eight arms at once in greeting. "
                    "He changed colour from purple to pink to gold — just to make Olivia giggle. "
                    "Then Stella the sea turtle glided past, smooth and slow as a dream, and let them rest on her wide, mossy shell."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "A flash of silver shot through the water — Ziggy the squid zoomed by trailing ribbons of light. "
                    "And then, very slowly, a great grey shape appeared from the shadows. "
                    "It was Finn the shark — but he had the kindest eyes Lucas had ever seen, and he bowed his head politely."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "All the sea friends gathered in a circle around the children. "
                    "The water glowed a soft blue-green, and everything felt peaceful and quiet. "
                    "Olivia leaned her head on Lucas's shoulder and yawned the tiniest yawn. "
                    "'Time to go home,' said Stella gently, and the submarine floated them slowly back to shore."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 6,
                "text": (
                    "Back in their warm beds, Lucas and Olivia smiled at the ceiling. "
                    "Outside, the stars shimmered like the lights of Bella, Inky, Stella, Ziggy, and Finn far below. "
                    "The deep sea was always there — waiting, sparkling, and full of friends — whenever they closed their eyes and dreamed."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
        ],
    },

    # ------------------------------------------------------------------
    # 8. Lucas and Olivia and the Dinosaur Valley
    # ------------------------------------------------------------------
    {
        "title": "Lucas and Olivia and the Dinosaur Valley",
        "theme_tags": ["dinosaurs", "adventure", "siblings", "magic"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 300,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "Lucas found an old golden compass under his pillow one night. "
                    "When he held it up, it spun wildly and a warm light poured from the window — pointing toward a misty valley neither child had ever seen. "
                    "Olivia pulled on her boots. 'Let's go,' she said, and they ran."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "The valley was lush and green, with giant ferns as tall as houses. "
                    "A small Triceratops with three wobbly horns waddled up and sniffed Olivia's hand. "
                    "'His name is Bumble,' said a voice — it was a tiny girl dinosaur in a flower crown who spoke perfect English and seemed very pleased to have visitors."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "Bumble led them to a wide, warm lake where a family of Brachiosaurus dipped their long necks to drink. "
                    "Lucas climbed onto Bumble's back and Olivia rode a friendly Ankylosaurus named Plum, whose armoured tail wagged like a dog's. "
                    "They rumbled happily through the valley as fireflies lit the fern tops gold."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "As the twin moons of Dinosaur Valley rose, the creatures all gathered in a great circle and hummed a low, rumbling lullaby. "
                    "The ground vibrated softly beneath the children's feet — a sound like a heartbeat, warm and steady. "
                    "Olivia closed her eyes and smiled. 'It feels like a hug,' she said."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "The compass glowed again, gently pulling them home. "
                    "Bumble pressed his great head against Lucas's chest for a long moment, then stepped back and blinked his big brown eyes slowly — which is how dinosaurs say goodnight. "
                    "Lucas and Olivia tiptoed back to bed, still warm from the valley's lullaby, and were asleep before they knew it."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
        ],
    },

    # ------------------------------------------------------------------
    # 9. Lucas, Olivia and the Meadow of Sleepy Rabbits
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia and the Meadow of Sleepy Rabbits",
        "theme_tags": ["rabbits", "nature", "siblings", "sleep"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 270,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "One spring evening, a white rabbit with a daisy behind her ear hopped to the children's window and tapped three times. "
                    "'My name is Clover,' she said. 'Our meadow needs two good helpers before bedtime — will you come?' "
                    "Lucas and Olivia were already in their pyjamas. They hopped right out after her."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "The meadow was silver in the moonlight, dotted with hundreds of tiny rabbits who had forgotten how to fall asleep. "
                    "Some were bouncing. Some were nibbling clover. Some were just looking at the sky with wide, worried eyes. "
                    "'We need a bedtime song,' said Clover. 'But none of us can remember the tune.'"
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "Olivia began to hum a soft tune — slow and gentle as a rocking boat. "
                    "One by one the rabbits stopped bouncing and sat very still, ears drooping with sleepiness. "
                    "Lucas gently tucked dandelion-fluff blankets around the tiniest ones, who were already nose-deep in the grass."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "Soon every single rabbit in the meadow was curled in a soft ball, breathing slowly and dreaming of carrots and sunshine. "
                    "Clover sat between Lucas and Olivia and let out a long, happy sigh. "
                    "'You did it,' she whispered. 'The meadow thanks you.'"
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "Clover led them back to their window and pressed a tiny warm pebble into each of their hands — the rabbits' gift for the kindest helpers. "
                    "That night Lucas and Olivia held their pebbles and felt the same gentle warmth as the meadow. "
                    "They closed their eyes, and the soft tune Olivia had hummed floated them right into the most peaceful dream."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
        ],
    },

    # ------------------------------------------------------------------
    # 10. The Snowman Who Needed a Name
    # ------------------------------------------------------------------
    {
        "title": "The Snowman Who Needed a Name",
        "theme_tags": ["snowman", "winter", "siblings", "magic"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 270,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "After a big snowfall, Lucas and Olivia built the finest snowman the garden had ever seen. "
                    "They gave him a carrot nose, two pinecone eyes, and a bright red scarf. "
                    "Then — just as they were about to go inside — the snowman blinked and said, very quietly, 'Hello.'"
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "'I've been waiting all winter for someone to make me,' said the snowman with a happy wobble. "
                    "'But I don't have a name. Could you help?' "
                    "Lucas and Olivia looked at each other. This was the most important job they had ever been given."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "They thought of names for a whole hour: Fluffy, Blizzard, Captain Carrot, Sir Snowsworth. "
                    "The snowman giggled at each one — a sound like sleigh bells — but shook his round head. "
                    "Then Olivia looked at his kind pinecone eyes and whispered, 'What about Cozy?' "
                    "The snowman went very still — and then glowed from inside like a warm lamp."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "'Cozy,' he repeated slowly, trying it out. 'Yes. That's exactly right.' "
                    "He told the children that now that he had a name, he would guard the garden every night while they slept. "
                    "He would watch the stars, hum to the snowflakes, and make sure nothing woke them till morning."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "That night, from their warm beds, Lucas and Olivia peeked through the frosted window. "
                    "Cozy stood in the garden, softly glowing, snowflakes drifting around him like tiny dancing stars. "
                    "He turned and gave them a slow, gentle wave. "
                    "They waved back, pulled their blankets up, and fell into the deepest, coziest sleep of their lives."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
        ],
    },

    # ------------------------------------------------------------------
    # 11. Happy, Wangcai and the Midnight Walk
    # ------------------------------------------------------------------
    {
        "title": "Happy, Wangcai and the Midnight Walk",
        "theme_tags": ["dogs", "night", "siblings", "friendship"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 270,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "Lucas and Olivia had two dogs: Happy, a fluffy golden dog who wagged his tail so fast it looked like wings, "
                    "and Wangcai, a chunky brown dog with a big round belly and a very dignified walk. "
                    "One night, both dogs put their paws on the children's beds and stared at them with wide, serious eyes."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "Happy barked once — soft, like a question. Wangcai sat very still, which meant something important. "
                    "'They want to show us something,' said Olivia. "
                    "The four of them tiptoed out into the moonlit garden, Happy bouncing and Wangcai waddling with great purpose."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "Happy led them to the old apple tree where a family of hedgehogs had made their bed among the roots. "
                    "Wangcai sat down beside them like a round, warm guard and let out a long, satisfied sigh. "
                    "The hedgehogs didn't stir — they had been sleeping soundly because Wangcai watched over them every night."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "Happy curled around Lucas and Olivia to keep them warm, his golden fur soft as a cloud. "
                    "Above them, the stars were very bright and the air smelled of apple blossom and fresh grass. "
                    "'This is the best secret in the whole garden,' whispered Lucas."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "One by one, they all walked back inside — Happy skipping, Wangcai waddling, the children yawning. "
                    "Both dogs curled at the foot of the beds, one on each side, warm and steady as two small suns. "
                    "Lucas and Olivia fell asleep listening to the quiet sound of their dogs breathing — the most comforting sound in the world."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
        ],
    },

    # ------------------------------------------------------------------
    # 12. Lucas, Olivia and the Paw Patrol to the Rescue
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia and the Paw Patrol to the Rescue",
        "theme_tags": ["paw patrol", "adventure", "siblings", "dogs"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 300,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "Lucas and Olivia were hiking up Sunset Hill when a big purple cloud rolled in and the trail lights flickered off. "
                    "Then they heard it — a familiar bark, and a flash of red and blue lights below. "
                    "The Paw Patrol Lookout was parked right at the base of the hill, and Ryder's voice called out: 'No job is too big, no pup is too small!'"
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "Chase zoomed up in his police cruiser, ears perked, tail wagging. "
                    "'Don't worry, Lucas — I'll light the path!' He switched on his police lights and the whole trail glowed safe and bright. "
                    "Skye swooped overhead in her helicopter, dropping a map and a gentle shower of sparkles that made Olivia laugh."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "Marshall raced up with his fire truck, carrying hot cocoa in a thermos. "
                    "Rubble drove his bulldozer to clear a cosy flat spot for everyone to sit. "
                    "Rocky arrived last with his recycling truck, pulling out soft blankets he had found and folded perfectly. "
                    "'Every pup does their part!' said Ryder proudly."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "All the pups and the two children sat together under the clearing sky, wrapped in blankets, sharing cocoa. "
                    "Zuma counted shooting stars and Everest spotted a constellation shaped like a paw print. "
                    "'That one's ours,' said Chase, and his tail wagged so hard the blanket slid off his back."
                ),
                "illustration_url": None,
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "When the children's eyes grew heavy, Skye's helicopter gently lifted them and carried them home — so smoothly they didn't even wake. "
                    "Ryder tucked them in and Chase sat beside the bed until their breathing was slow and deep. "
                    "'Mission complete,' Ryder whispered with a smile. "
                    "And every pup gave one last quiet bark — goodnight."
                ),
                "illustration_url": None,
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
