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
    # ------------------------------------------------------------------
    # 13. The Rainbow Bridge
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy and the Rainbow Bridge",
        "theme_tags": ["adventure", "unicorn", "animals", "friendship"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 300,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "One sunny afternoon, Lucas, Olivia, and their dog Happy were playing in the garden. "
                    "Suddenly Olivia's unicorn, Sparkle, galloped over with her mane shimmering like moonlight. "
                    "'Come quickly!' Sparkle cried. 'A rainbow bridge has appeared over Bluebell Hill!'"
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "Happy bounded ahead, his golden tail wagging like a flag in the wind. "
                    "Lucas ran to keep up, and Olivia held on to Sparkle's silky mane as they trotted up the hill. "
                    "When they reached the top, a glittering bridge of red, orange, yellow, green, blue, and violet stretched across the sky."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "At the foot of the bridge sat a tiny cloud-bunny with fluffy white ears and worried eyes. "
                    "'My cloud castle blew away,' the bunny sniffled. 'I can't find my way home.' "
                    "Happy gently licked the bunny's cheek, and the bunny giggled at last."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "Sparkle knelt so the cloud-bunny could climb onto her back. "
                    "Together the four friends — Lucas, Olivia, Happy, and Sparkle — walked across the shimmering rainbow bridge. "
                    "The colours hummed softly like a lullaby under their feet."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "At the other end floated a fluffy white castle made of clouds. "
                    "The cloud-bunny leapt off Sparkle's back and hugged every one of them. "
                    "'Thank you, dear friends! You will always have a home here in the sky.' "
                    "Happy barked happily, and the castle filled with soft golden light."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 6,
                "text": (
                    "As the sun dipped low and painted the sky pink, the friends walked home across the rainbow. "
                    "Lucas held Olivia's hand, Happy trotted beside them, and Sparkle hummed a gentle tune. "
                    "By the time they reached their garden, they were yawning and their eyes were drooping with lovely, happy dreams."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
        ],
    },
    # ------------------------------------------------------------------
    # 14. The Hidden Treasure Map
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy and the Hidden Treasure Map",
        "theme_tags": ["adventure", "treasure", "animals", "unicorn"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 300,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "Happy was digging in the garden — as dogs do — when his paw hit something hard. "
                    "He barked until Lucas and Olivia came running. "
                    "There in the dirt was an old rolled-up map tied with a golden ribbon."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "Olivia unrolled the map carefully. It showed a winding path through the Whispering Woods "
                    "that led to a big red X near the old oak tree. "
                    "'Treasure!' Lucas shouted, already pulling on his boots."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "Sparkle the unicorn used her glowing horn to light the way as they entered the Whispering Woods. "
                    "The trees swayed hello and fireflies blinked like tiny lanterns all around them. "
                    "Happy's nose twitched — he could already smell something wonderful."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "They crossed a mossy bridge, climbed a gentle hill, and found the ancient oak tree. "
                    "Happy dug eagerly while Lucas and Olivia held the map. "
                    "Soon his paws hit a wooden chest with a shiny brass latch."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "Inside the chest were four things: a sparkling star for Olivia, "
                    "a tiny compass for Lucas, a jingle-bell collar for Happy, "
                    "and a flower-crown that fit perfectly on Sparkle's horn. "
                    "'The treasure knew exactly what we each needed!' Olivia laughed."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 6,
                "text": (
                    "They walked home through the moonlit woods, Happy's new bell jingling softly with every step. "
                    "Olivia held her star up to the sky and it glowed right back at the real stars above. "
                    "Lucas whispered, 'Best adventure ever,' and Happy and Sparkle agreed with a bark and a gentle whinny."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
        ],
    },
    # ------------------------------------------------------------------
    # 15. The Storm That Turned Into a Song
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy and the Storm That Turned Into a Song",
        "theme_tags": ["adventure", "unicorn", "animals", "stars"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 300,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "A big grey cloud rolled over the meadow and thunder rumbled like a tummy growl. "
                    "Happy hid under the picnic blanket and peeked out with one eye. "
                    "'Don't worry, Happy,' said Lucas, snuggling close. 'We'll figure this out together.'"
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "Sparkle stepped forward and touched her glowing horn to the dark cloud. "
                    "The cloud trembled and let out a long, low note — like a sad song that had never been sung. "
                    "'The cloud is lonely,' Olivia said softly. 'It just wants someone to listen.'"
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "So Olivia began to hum, and Lucas tapped a rhythm on the picnic basket. "
                    "Happy howled a happy howl that bounced off the hills. "
                    "The cloud's thunder turned softer, then gentler, and little raindrops fell like a slow, steady drum."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "The raindrops became part of the song, tip-tapping on the leaves above them. "
                    "Sparkle swayed her silver mane in time. "
                    "The big grey cloud began to glow pink and gold at its edges, joining in at last."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "When the song ended, the cloud drifted away smiling, leaving a glittering rainbow behind it. "
                    "Happy shook the last drops from his fluffy ears and barked cheerfully. "
                    "The sun came back, warm and golden, and dried every bit of the meadow."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 6,
                "text": (
                    "That night, Lucas and Olivia lay on the soft grass and counted the stars appearing one by one. "
                    "Happy curled up between them, and Sparkle stood close, her horn glowing like a soft nightlight. "
                    "The sky hummed the cloud's song back to them very, very quietly, and they drifted off to sleep."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
        ],
    },
    # ------------------------------------------------------------------
    # 16. The Cloud-Painting Competition
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy and the Cloud-Painting Competition",
        "theme_tags": ["adventure", "unicorn", "animals", "stars"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 300,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "High above the meadow, the Cloud-Painters were getting ready for their yearly competition. "
                    "Each team had to paint the most beautiful sunset cloud before the moon arrived. "
                    "A small cloud messenger floated down and invited Lucas, Olivia, Happy, and Sparkle to join."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "Sparkle carried them all up on her back, galloping right into the sky. "
                    "The clouds were soft and bouncy under their feet, like the world's fluffiest trampoline. "
                    "Happy rolled around in a fluffy cloud-pile while Lucas and Olivia chose their rainbow paint-pots."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "Lucas painted a giant golden sun sinking slowly into a pink sea. "
                    "Olivia added purple mountains and a tiny unicorn silhouette on top. "
                    "Happy dipped his paw in orange paint and added pawprint stamps all along the bottom, which made everyone laugh."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "Sparkle touched her horn to the cloud-painting and it began to shimmer and glow. "
                    "The colours swirled and sparkled, and tiny stars appeared inside it all by themselves. "
                    "The other Cloud-Painters gasped with wonder."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "When the moon arrived to judge, she looked at every painting very carefully. "
                    "Then she smiled her crescent smile and said, 'This one — with the pawprints and the stars — warms my heart the most.' "
                    "Happy barked proudly and did a little spin."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 6,
                "text": (
                    "The moon hung their painting right in the evening sky for everyone below to see. "
                    "Sparkle glided them gently back down to their garden as the stars came out one by one. "
                    "Lucas, Olivia, and Happy looked up at their glowing cloud-painting and felt perfectly, completely happy."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
        ],
    },
    # ------------------------------------------------------------------
    # 17. The Tiny Island in the Bathtub Sea
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy and the Tiny Island in the Bathtub Sea",
        "theme_tags": ["adventure", "ocean", "unicorn", "animals"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 300,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "One rainy afternoon, Lucas filled the bathtub to the very brim and declared it the Bathtub Sea. "
                    "Olivia placed their toy boat in the water and named it the S.S. Sparkle. "
                    "Happy sat on the bathmat as captain, wearing a paper hat Lucas had folded for him."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "Then something magical happened — Sparkle the unicorn shrank to the size of a rubber duck "
                    "and stepped right onto the boat! "
                    "'The Bathtub Sea is real today,' she said in a tiny, silvery voice. 'Sail to the island at the far end!'"
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "They sailed past a bubble-reef full of tiny soap-fish that blew shimmering bubbles into the air. "
                    "Happy paddled alongside the boat, his tail acting as the rudder. "
                    "The rubber-duck fleet honked a friendly greeting as they passed."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "At the far end of the bathtub stood a tiny island made of a washcloth and three stacked soap bars. "
                    "A family of bath-toy animals lived there: a pink elephant, a green frog, and a yellow giraffe. "
                    "'Welcome, explorers!' they cheered."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "The bath-toy animals had built a whole little village with toothpaste towers and shampoo-bottle lighthouses. "
                    "They shared a feast of foam-strawberries and bubble-grapes. "
                    "Happy ate three helpings and licked his nose clean."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 6,
                "text": (
                    "When the water began to cool, Sparkle grew back to her full size and gently lifted Lucas and Olivia out. "
                    "Happy shook the water from his fur and curled up on the warm towel. "
                    "As they drifted off to sleep, they could still hear the tiny lighthouse sending its soft, blinking light into the dark."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
        ],
    },
    # ------------------------------------------------------------------
    # 18. The Mountain of a Thousand Echoes
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy and the Mountain of a Thousand Echoes",
        "theme_tags": ["adventure", "forest", "unicorn", "animals"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 300,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "On a clear morning, Sparkle noticed a tall mountain in the distance that hadn't been there the day before. "
                    "'That's the Mountain of a Thousand Echoes,' she said. 'It only appears once a year, and today is the day.' "
                    "Lucas grabbed his backpack, Olivia tucked a sandwich inside, and Happy wagged his tail three times fast."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "The mountain was covered in soft purple heather that hummed when you walked through it. "
                    "Every sound they made — a laugh, a bark, a clip of Sparkle's hooves — bounced back from the rocks in a beautiful echo. "
                    "Happy barked and heard himself bark back nine times, getting quieter and sweeter each time."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "Near the middle of the mountain, they found a cave where all the echoes gathered and lived. "
                    "The echoes floated like little bubbles of sound, each one holding a laugh or a word from someone long ago. "
                    "'Listen,' Olivia whispered. 'I can hear a lullaby.'"
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "The lullaby was old and soft, sung by someone who loved their children very much. "
                    "Sparkle hummed along, and her magic made the echoes glow gold and float up through the cave roof like fireflies. "
                    "Lucas and Olivia held hands and listened until the song was done."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "At the very top of the mountain was a glass bowl where new echoes could be left forever. "
                    "Lucas sang a joke. Olivia whispered 'I love you.' Happy howled his best howl. "
                    "Sparkle added a single clear note that rang like a silver bell."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 6,
                "text": (
                    "They made their way back down as the mountain began to fade softly into the evening mist. "
                    "Happy walked slowly now, pleasantly tired, his ears drooping in the nicest way. "
                    "That night, Lucas and Olivia fell asleep to the faint sound of their own echoes floating back to them on the breeze."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
        ],
    },
    # ------------------------------------------------------------------
    # 19. The Night Market in the Garden
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy and the Night Market in the Garden",
        "theme_tags": ["adventure", "stars", "unicorn", "animals"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 300,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "One evening, tiny lanterns appeared all over the garden — red, gold, blue, and green. "
                    "Lucas pressed his nose to the window. 'There's a market out there!' "
                    "Olivia grabbed Sparkle's mane, Happy pressed his nose to the glass beside Lucas, and they all hurried outside."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "The Night Market was run by garden creatures: hedgehogs selling dewdrop lemonade, "
                    "fireflies offering jars of their own gentle light, "
                    "and a wise old tortoise who traded riddles for moonstone pebbles."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "Happy traded a friendly lick for a hedgehog biscuit shaped like a bone. "
                    "Lucas answered the tortoise's riddle — 'What has hands but no arms? A clock!' — and won two moonstones. "
                    "Olivia bought a firefly lantern that blinked in time with her heartbeat."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "Sparkle's favourite stall was the flower-crown weaver, a tiny spider who worked with moonbeam thread. "
                    "She wove a crown of lavender and silver stars for Sparkle's horn in less than a minute. "
                    "It glimmered so beautifully that all the fireflies gathered around to admire it."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "As the market began to pack away, the tortoise gathered everyone for a last dance. "
                    "The fireflies hummed a waltz, the hedgehogs tapped their tiny feet, and even the moonflowers swayed. "
                    "Lucas and Olivia danced together, laughing, while Happy spun in happy circles."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 6,
                "text": (
                    "By the time the last lantern went out, Lucas and Olivia could barely keep their eyes open. "
                    "Sparkle carried them gently to the back door, and Happy led the way up the stairs. "
                    "Olivia's firefly lantern blinked softly on the bedside table, a tiny light guarding them all through the night."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
        ],
    },
    # ------------------------------------------------------------------
    # 20. The Frozen Lake and the Ice Sprites
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy and the Frozen Lake and the Ice Sprites",
        "theme_tags": ["adventure", "stars", "unicorn", "animals"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 300,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "Winter had arrived in the night, and by morning the little pond at the bottom of the garden "
                    "had frozen into a perfect mirror of ice. "
                    "Lucas slid across it first, spinning like a top. Happy ran after him and slid much, much further, crashing gently into a snowdrift."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "Sparkle stepped onto the ice very carefully, and where her hooves touched, "
                    "tiny flowers of frost bloomed in the most beautiful patterns. "
                    "Olivia knelt to look closely and found tiny creatures living inside the frost flowers — Ice Sprites, no bigger than a thumb."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "The Ice Sprites were building a tiny city under the ice, "
                    "with crystal towers and bridges made of frozen droplets. "
                    "'We only have until the sun gets too warm,' the smallest sprite said. "
                    "'Please help us finish before we melt away!'"
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "Sparkle used her magic to keep the ice perfectly cold. "
                    "Happy used his big gentle paws to carefully push snowflakes into the right shape. "
                    "Lucas and Olivia used their fingers to press tiny windows into the crystal towers."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "By midday the ice city was finished, gleaming and sparkling under the winter sun. "
                    "All the Ice Sprites cheered a tiny cheer that sounded like the tinkling of small bells. "
                    "They gave each friend a gift: a snowflake that would never melt, kept safe in a little glass bottle."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 6,
                "text": (
                    "That evening, the four friends sat by the fire with warm cocoa and looked at their snowflakes glowing softly in the firelight. "
                    "Happy leaned his head against Lucas's leg and sighed a long, cosy sigh. "
                    "Olivia placed her snowflake beside her pillow, and as the fire crackled low, they all fell fast asleep."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
        ],
    },
    # ------------------------------------------------------------------
    # 21. The Library at the End of the Garden
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy and the Library at the End of the Garden",
        "theme_tags": ["adventure", "forest", "unicorn", "animals"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 300,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "One afternoon, Happy started digging at the very end of the garden — further than he had ever dug before. "
                    "He disappeared into the hole, then poked his head back up with a look of pure amazement. "
                    "Lucas and Olivia followed him in and found themselves inside a cosy underground library lit by glowing mushrooms."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "The shelves went up and up and up, higher than they could see, filled with books of every colour. "
                    "Sparkle — who had shrunk to fit through the tunnel — ran her horn along the spines "
                    "and each book hummed the first line of its story aloud."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "A mole with round gold spectacles was the librarian. "
                    "'You may each borrow one story to dream tonight,' she said with a warm smile. "
                    "Lucas chose a story about rockets. Olivia chose a story about a princess who fixed machines. "
                    "Happy chose a story about a dog who baked cakes — of course."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "The mole-librarian showed them the Reading Nook, a hollow tree-root lined with the softest moss. "
                    "Sparkle read all three stories aloud in her gentle voice while the mushrooms glowed warmer and warmer. "
                    "Happy rested his chin on Lucas's knee and listened with his eyes half-closed."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "When the stories were finished, the books tucked themselves neatly back onto their shelves. "
                    "The mole-librarian stamped a tiny star on each of their hands — the library's way of saying 'come back soon.' "
                    "Happy's stamp was on his paw, and he kept sniffing it the whole way home."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 6,
                "text": (
                    "Back in their beds, Lucas dreamed of racing among the stars, and Olivia dreamed of her princess fixing a golden clock. "
                    "Happy dreamed of a cake shaped like a bone covered in gravy icing. "
                    "And somewhere deep in the garden, the library glowed on quietly, waiting for them to return."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
        ],
    },
    # ------------------------------------------------------------------
    # 22. The Balloon That Flew to the Moon
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy and the Balloon That Flew to the Moon",
        "theme_tags": ["adventure", "space", "unicorn", "animals", "stars"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 300,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {
                "page_number": 1,
                "text": (
                    "A giant silver balloon appeared in the garden, tied to the garden gate with a ribbon of starlight. "
                    "A note said: 'For brave explorers only. Seats: four.' "
                    "Lucas read it twice, Olivia clapped her hands, Happy pressed his paws on the side of the basket, and Sparkle arched her neck in excitement."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 2,
                "text": (
                    "The balloon lifted off gently, carried by a warm, rose-scented breeze. "
                    "Below them the garden grew smaller, then the town, then the whole country. "
                    "Happy pressed his nose to the edge of the basket and sniffed the clouds — they smelled like fresh cotton and rain."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 3,
                "text": (
                    "They floated past a flock of moon-birds — white birds with feathers that caught the starlight. "
                    "The birds sang as they flew alongside, a soft travelling-song that made the basket feel warm and safe. "
                    "Sparkle sang back, and the moon-birds swooped in delight."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 4,
                "text": (
                    "The Moon herself was waiting when they arrived — large and round and gently glowing. "
                    "She had set out a table of moonberry pie and silver-milk, and she smiled as they stepped out of the basket. "
                    "'I always hoped someone would come for supper,' she said."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 5,
                "text": (
                    "They ate and talked and laughed with the Moon as the stars came out one by one around them. "
                    "Happy fell asleep under the table with a moonberry on his nose. "
                    "The Moon covered him with a cloud-blanket and whispered, 'Sleep well, brave dog.'"
                ),
                "illustration_url": "",
                "audio_url": None,
            },
            {
                "page_number": 6,
                "text": (
                    "The balloon carried them home just as dawn was painting the sky the palest pink. "
                    "Lucas and Olivia were back in their beds before the alarm clock even thought about ringing. "
                    "Happy curled up at the foot of the bed, and Sparkle stood by the window, watching the Moon fade gently into the morning light."
                ),
                "illustration_url": "",
                "audio_url": None,
            },
        ],
    },
    # ------------------------------------------------------------------
    # 23. Peppa Pig
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy, Rabbit and Peppa's Muddy Puddle Day",
        "theme_tags": ["animals", "adventure", "friendship"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 240,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {"page_number": 1, "text": "Lucas, Olivia, Happy the dog, and their little rabbit Clover went to the park. They found Peppa Pig and her little brother George jumping in muddy puddles. 'Come in!' said Peppa. 'Muddy puddles are the best!'", "illustration_url": "", "audio_url": None},
            {"page_number": 2, "text": "Happy jumped in first — SPLASH! Mud went everywhere. Clover the rabbit hopped in next, her long ears flopping. George squealed with joy and jumped in with both feet.", "illustration_url": "", "audio_url": None},
            {"page_number": 3, "text": "Lucas tried the biggest puddle. SPLOSH! Mud flew up to his nose. Olivia laughed so hard she fell right in too. Everyone was brown from head to toe.", "illustration_url": "", "audio_url": None},
            {"page_number": 4, "text": "Peppa's daddy came with a big hose. He washed everyone clean while they giggled and squealed. Happy shook himself dry and got everyone wet all over again.", "illustration_url": "", "audio_url": None},
            {"page_number": 5, "text": "They all sat on the grass and ate muddy-puddle-shaped biscuits Peppa had brought. Clover got extra carrots. Happy got a big dog biscuit. Everyone had the muddiest, happiest day.", "illustration_url": "", "audio_url": None},
            {"page_number": 6, "text": "On the way home, Lucas said, 'That was the best puddle day ever.' Olivia nodded. Happy wagged. Clover closed her eyes. They were home and in bed before the mud had even dried on their boots.", "illustration_url": "", "audio_url": None},
        ],
    },
    # ------------------------------------------------------------------
    # 24. Bluey
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy, Rabbit and a Game with Bluey",
        "theme_tags": ["animals", "adventure", "friendship"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 240,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {"page_number": 1, "text": "Bluey the blue heeler puppy knocked on the door. 'Want to play Calypso?' she said. Lucas and Olivia said yes right away. Happy barked and Clover the rabbit bounced with excitement.", "illustration_url": "", "audio_url": None},
            {"page_number": 2, "text": "Bluey made up the rules as she went. First, everyone had to walk like a crab. Happy found this very hard. Clover was surprisingly good at it. Olivia could not stop laughing.", "illustration_url": "", "audio_url": None},
            {"page_number": 3, "text": "Then Bluey said they had to hop on one foot while counting backwards from ten. Lucas got to seven before falling on the soft grass. Bluey cheered anyway.", "illustration_url": "", "audio_url": None},
            {"page_number": 4, "text": "Next was the quiet game. Everyone had to be silent for one whole minute. Happy lasted four seconds before barking at a butterfly. Clover won easily because rabbits are very good at being quiet.", "illustration_url": "", "audio_url": None},
            {"page_number": 5, "text": "For the last game, Bluey's dad Bandit chased them all around the garden. They screamed and ran and hid behind the big bush. Happy hid under Bandit's feet by mistake.", "illustration_url": "", "audio_url": None},
            {"page_number": 6, "text": "At the end, they all lay on their backs in the garden and looked at the evening sky. 'Good game,' said Bluey. 'Best game,' said Lucas. One by one, their eyes slowly closed.", "illustration_url": "", "audio_url": None},
        ],
    },
    # ------------------------------------------------------------------
    # 25. Cocomelon
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy, Rabbit and a Song with JJ",
        "theme_tags": ["animals", "adventure", "friendship"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 240,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {"page_number": 1, "text": "JJ was a little boy with a round happy face. He came to play with Lucas and Olivia, their dog Happy, and their rabbit Clover. 'Let's sing!' said JJ. He always wanted to sing.", "illustration_url": "", "audio_url": None},
            {"page_number": 2, "text": "JJ started with the alphabet song. Happy tried to sing along and howled on every letter A. Clover thumped her foot in time. Lucas and Olivia clapped along.", "illustration_url": "", "audio_url": None},
            {"page_number": 3, "text": "Then they sang a bath-time song. Happy ran straight to the paddling pool and jumped in. Water went everywhere. JJ laughed until his round little tummy shook.", "illustration_url": "", "audio_url": None},
            {"page_number": 4, "text": "Next came the vegetable song. Olivia made a carrot crown for Clover. Lucas made a broccoli wand. JJ made up a silly verse about potatoes that made no sense but everyone loved it.", "illustration_url": "", "audio_url": None},
            {"page_number": 5, "text": "For the last song, JJ led the sleepy-time song very slowly. The tune was soft and low. Happy's tail wagged more and more slowly. Clover's eyes began to close.", "illustration_url": "", "audio_url": None},
            {"page_number": 6, "text": "By the end of the song, all five of them — Lucas, Olivia, Happy, Clover, and JJ — were curled up on the rug together. The sun set softly and the room went warm and quiet.", "illustration_url": "", "audio_url": None},
        ],
    },
    # ------------------------------------------------------------------
    # 26. Tinga Tinga Tales
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy, Rabbit and the Tinga Tinga Animals",
        "theme_tags": ["animals", "adventure", "friendship", "forest"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 240,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {"page_number": 1, "text": "One morning, a bright painted door appeared in the garden wall. Lucas opened it and found the colourful world of Tinga Tinga. Everything was bright and bold — red, yellow, blue, and green.", "illustration_url": "", "audio_url": None},
            {"page_number": 2, "text": "Elephant came first, her big ears bright orange. She showed Happy how to spray water with her trunk. Happy tried to copy her using his water bowl and got completely soaked.", "illustration_url": "", "audio_url": None},
            {"page_number": 3, "text": "Zebra trotted over with his bold black and white stripes. Clover the rabbit looked at the stripes very carefully. She tried to paint her own stripes with mud. She looked very silly and very happy.", "illustration_url": "", "audio_url": None},
            {"page_number": 4, "text": "Giraffe stretched her long neck down to say hello to Olivia. Olivia stood on her tiptoes to whisper a secret: 'You have the most beautiful spots I have ever seen.' Giraffe smiled and blushed.", "illustration_url": "", "audio_url": None},
            {"page_number": 5, "text": "Lion told them the story of why Lion roars. He puffed up his chest and let out a big roar. Happy roared back with his best bark. The whole Tinga Tinga world shook with laughter.", "illustration_url": "", "audio_url": None},
            {"page_number": 6, "text": "When the sun began to set over Tinga Tinga, the animals sang a soft evening song together. Lucas and Olivia hummed along. Happy lay at their feet. Clover was already asleep. They tiptoed back through the painted door and into their own warm home.", "illustration_url": "", "audio_url": None},
        ],
    },
    # ------------------------------------------------------------------
    # 27. Helper Cars
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy, Rabbit and the Helper Cars",
        "theme_tags": ["adventure", "animals", "friendship"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 240,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {"page_number": 1, "text": "The Helper Cars drove up the street with their lights on. There was a red fire engine, a yellow digger, a blue police car, and a green ambulance. They all beeped hello to Lucas, Olivia, Happy, and Clover.", "illustration_url": "", "audio_url": None},
            {"page_number": 2, "text": "The fire engine asked Lucas to help wash her. Lucas got the big sponge. Happy jumped in the bucket of soapy water and made a huge mess. The fire engine laughed a big fire-engine laugh — HONK HONK.", "illustration_url": "", "audio_url": None},
            {"page_number": 3, "text": "The yellow digger needed help moving a big pile of sand. Olivia scooped with her little spade. Clover dug alongside with her strong back feet. Together they moved the whole pile in no time.", "illustration_url": "", "audio_url": None},
            {"page_number": 4, "text": "The police car taught them about road safety. 'Always look both ways,' she said. Happy looked left, then right, then left again — very carefully. The police car gave him a tiny gold star sticker.", "illustration_url": "", "audio_url": None},
            {"page_number": 5, "text": "The green ambulance showed them how to take care of a tiny bird that had hurt its wing. Olivia made a soft nest from a scarf. The bird chirped thank you and flew away when it felt better.", "illustration_url": "", "audio_url": None},
            {"page_number": 6, "text": "As the Helper Cars drove off into the sunset, they beeped their horns in a little song. Lucas and Olivia waved until they could not see the lights anymore. Happy wagged. Clover yawned. It was time for bed.", "illustration_url": "", "audio_url": None},
        ],
    },
    # ------------------------------------------------------------------
    # 28. Octonauts
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy, Rabbit and the Octonauts",
        "theme_tags": ["ocean", "adventure", "animals", "friendship"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 240,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {"page_number": 1, "text": "The Octopod surfaced in the paddling pool. Captain Barnacles waved from the hatch. 'We need your help!' he called. Lucas, Olivia, Happy, and Clover looked at each other and grinned. Adventure time!", "illustration_url": "", "audio_url": None},
            {"page_number": 2, "text": "Kwazii the cat pirate gave everyone a little wetsuit. Happy's had a hole for his tail. Clover's had holes for her long ears. They all looked very official.", "illustration_url": "", "audio_url": None},
            {"page_number": 3, "text": "Deep below the pool — which was much deeper on the inside — a family of tiny glowing starfish had lost their way home. Peso the penguin medic checked them all over to make sure they were safe.", "illustration_url": "", "audio_url": None},
            {"page_number": 4, "text": "Shellington the otter showed Lucas and Olivia his charts. Together they found the starfish's rocky home. Happy swam ahead, his tail acting like a propeller. Clover held the torch.", "illustration_url": "", "audio_url": None},
            {"page_number": 5, "text": "They guided the starfish family through the kelp and over the coral until they reached their warm rock. The starfish lit up bright pink to say thank you. The whole ocean glowed.", "illustration_url": "", "audio_url": None},
            {"page_number": 6, "text": "Back on the surface, Captain Barnacles gave everyone an Octonaut badge. Happy wore his on his collar. Clover wore hers on her ear. Lucas and Olivia pinned theirs to their pyjamas. They fell asleep dreaming of the deep blue sea.", "illustration_url": "", "audio_url": None},
        ],
    },
    # ------------------------------------------------------------------
    # 29. Mixed Adventure 1 — Peppa + Bluey
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy, Rabbit, Peppa and Bluey's Big Picnic",
        "theme_tags": ["animals", "adventure", "friendship"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 240,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {"page_number": 1, "text": "Peppa Pig brought sandwiches. Bluey brought a ball and three made-up games. Lucas brought juice. Olivia brought biscuits shaped like stars. Happy brought his favourite stick. Clover brought a carrot she had been saving for just this day.", "illustration_url": "", "audio_url": None},
            {"page_number": 2, "text": "Bluey's first game was Statue. Everyone had to freeze when she called 'STOP!' Happy was the worst at it. He froze — but his tail kept wagging all by itself. He could not help it.", "illustration_url": "", "audio_url": None},
            {"page_number": 3, "text": "Peppa found the biggest puddle in the park. They all took turns jumping. Clover made the tiniest splash. Happy made the biggest. The sandwiches got a little bit muddy but they ate them anyway.", "illustration_url": "", "audio_url": None},
            {"page_number": 4, "text": "After lunch, Bluey led a cloud-watching game. She said one cloud looked like a dragon. Peppa said it looked like a sausage. Lucas said it looked like a spaceship. Olivia said it looked like all three at once.", "illustration_url": "", "audio_url": None},
            {"page_number": 5, "text": "As the afternoon grew soft and warm, Bluey made up a slow, quiet game. Everyone had to whisper everything. Even Happy whispered his barks — tiny little 'wuf wuf wufs' that made everyone smile.", "illustration_url": "", "audio_url": None},
            {"page_number": 6, "text": "They packed up the picnic as the sky turned pink. On the walk home, Peppa held Olivia's hand and Bluey walked beside Lucas. Happy carried the empty basket. Clover rode on Happy's back. Best picnic ever.", "illustration_url": "", "audio_url": None},
        ],
    },
    # ------------------------------------------------------------------
    # 30. Mixed Adventure 2 — JJ + Tinga Tinga
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy, Rabbit, JJ and the Singing Safari",
        "theme_tags": ["animals", "adventure", "friendship", "forest"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 240,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {"page_number": 1, "text": "JJ arrived with his little backpack and a big smile. 'I know a song for every animal,' he said. Olivia thought that was wonderful. Happy thought that sounded like a challenge. They set off into the bright Tinga Tinga world.", "illustration_url": "", "audio_url": None},
            {"page_number": 2, "text": "When they met Elephant, JJ sang the elephant song. Elephant swayed and lifted her trunk. Happy howled along on the low notes. Clover thumped the beat with her back foot.", "illustration_url": "", "audio_url": None},
            {"page_number": 3, "text": "Giraffe needed a song with very high notes. JJ tried his best and squeaked on the top ones. Giraffe laughed and tried to sing too. Lucas said it sounded like a beautiful, very tall song.", "illustration_url": "", "audio_url": None},
            {"page_number": 4, "text": "Zebra wanted a stripy song — one note for black, one note for white, over and over. Olivia clapped the pattern. JJ sang it perfectly. Clover did a little stripey dance between the notes.", "illustration_url": "", "audio_url": None},
            {"page_number": 5, "text": "At sunset, all the Tinga Tinga animals gathered in a big circle. JJ led everyone in the goodnight song. It was slow and warm. The colours of Tinga Tinga softened as the sky turned gold.", "illustration_url": "", "audio_url": None},
            {"page_number": 6, "text": "They walked home through the painted door singing the last verse very quietly. JJ's eyes were half closed. Happy's tail did one last slow wag. Clover was already asleep in Olivia's arms. The night was soft and still.", "illustration_url": "", "audio_url": None},
        ],
    },
    # ------------------------------------------------------------------
    # 31. Mixed Adventure 3 — Helper Cars + Octonauts
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy, Rabbit, the Helper Cars and the Octonauts Save the Day",
        "theme_tags": ["adventure", "ocean", "animals", "friendship"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 240,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {"page_number": 1, "text": "A big storm had blown sand into the Octopod's docking bay. The Octonauts called the Helper Cars for help. Lucas, Olivia, Happy, and Clover came along too because every big job needs good friends.", "illustration_url": "", "audio_url": None},
            {"page_number": 2, "text": "The yellow digger scooped sand while Shellington measured how much was left. Happy carried buckets. Clover patted the sand flat with her strong back feet. 'Excellent teamwork!' said Captain Barnacles.", "illustration_url": "", "audio_url": None},
            {"page_number": 3, "text": "Then the fire engine pumped clean seawater to wash the Octopod's windows. Kwazii polished them with a big cloth. Lucas and Olivia squeegeed the bottom bits. The windows sparkled like crystals.", "illustration_url": "", "audio_url": None},
            {"page_number": 4, "text": "Peso found a little crab who had got stuck in the propeller. He gently set it free. The crab waved one claw in thanks and scuttled off sideways. Happy tried to wave sideways too. He fell over.", "illustration_url": "", "audio_url": None},
            {"page_number": 5, "text": "With the docking bay clean, the Octopod could dive again. The Helper Cars beeped their horns in a farewell fanfare. The Octonauts waved from the hatch. Lucas, Olivia, Happy, and Clover cheered from the shore.", "illustration_url": "", "audio_url": None},
            {"page_number": 6, "text": "That night, Lucas drew a picture of everyone working together. Olivia wrote all their names underneath. Happy sniffed the page proudly. Clover sat in the middle of the drawing, right where she always liked to be.", "illustration_url": "", "audio_url": None},
        ],
    },
    # ------------------------------------------------------------------
    # 32. All together — grand finale
    # ------------------------------------------------------------------
    {
        "title": "Lucas, Olivia, Happy, Rabbit and All Their Friends' Sleepover Party",
        "theme_tags": ["animals", "adventure", "friendship", "stars"],
        "is_curated": True,
        "is_ai_generated": False,
        "duration_seconds": 300,
        "created_for_child_id": None,
        "created_at": datetime.utcnow(),
        "pages": [
            {"page_number": 1, "text": "Lucas and Olivia sent invitations to all their friends. Peppa and George came. Bluey came. JJ came with his whole family. The Tinga Tinga animals peeked through the garden gate. The Helper Cars parked outside. The Octonauts arrived in the Octopod.", "illustration_url": "", "audio_url": None},
            {"page_number": 2, "text": "Happy ran around greeting everyone at once. Clover bounced so fast she was just a blur. The garden had fairy lights and blankets and pillows everywhere. It looked like the cosiest place in the whole world.", "illustration_url": "", "audio_url": None},
            {"page_number": 3, "text": "JJ led everyone in a big singalong. Bluey made up a game where you had to sing and spin at the same time. Peppa and George found a puddle by the fountain. Elephant trumpeted the chorus.", "illustration_url": "", "audio_url": None},
            {"page_number": 4, "text": "Captain Barnacles told a sea story by starlight. The Helper Cars' headlights made a warm glow. The Tinga Tinga animals formed a circle around the littlest ones to keep them cosy.", "illustration_url": "", "audio_url": None},
            {"page_number": 5, "text": "One by one, friends curled up on their blankets. George fell asleep hugging his toy dinosaur. Clover tucked in beside Happy. JJ's eyes closed mid-song. Bluey said 'goodnight' to each star she could count.", "illustration_url": "", "audio_url": None},
            {"page_number": 6, "text": "Lucas and Olivia were the last ones awake. They looked around at all their sleeping friends — old ones and new ones, furry ones and scaly ones, big ones and tiny ones. 'We're so lucky,' said Olivia. 'We really are,' said Lucas. Then they closed their eyes too.", "illustration_url": "", "audio_url": None},
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
