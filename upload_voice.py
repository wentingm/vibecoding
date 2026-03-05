#!/usr/bin/env python3
"""Upload a voice recording to ElevenLabs and save the Voice ID to .env"""

import os
import sys
import httpx
from dotenv import load_dotenv

load_dotenv("backend/.env")

API_KEY = os.getenv("ELEVENLABS_API_KEY", "")
if not API_KEY:
    print("❌ No ElevenLabs API key found in backend/.env")
    sys.exit(1)

# Find the recording file
audio_file = "voice_recording.wav"
if len(sys.argv) > 1:
    audio_file = sys.argv[1]

if not os.path.exists(audio_file):
    print(f"❌ File not found: {audio_file}")
    print("Run python3 record_voice.py first to record your voice.")
    sys.exit(1)

label = input("Is this Mom or Dad? (Mom/Dad): ").strip().capitalize()
if label not in ("Mom", "Dad"):
    label = "Mom"

print(f"\n📤 Uploading {audio_file} to ElevenLabs as '{label}'...")

with open(audio_file, "rb") as f:
    audio_data = f.read()

print(f"   File size: {len(audio_data)/1024:.0f} KB")

with httpx.Client(timeout=60) as client:
    resp = client.post(
        "https://api.elevenlabs.io/v1/voices/add",
        headers={"xi-api-key": API_KEY},
        data={"name": f"{label} - Bedtime Stories"},
        files={"files": (os.path.basename(audio_file), audio_data, "audio/wav")},
    )
    resp.raise_for_status()
    voice_id = resp.json()["voice_id"]

print(f"\n✅ Voice cloned! Voice ID: {voice_id}")

# Save to .env
env_path = "backend/.env"
with open(env_path, "r") as f:
    env = f.read()

field = "ELEVENLABS_VOICE_ID"
if field in env:
    import re
    env = re.sub(rf"{field}=.*", f"{field}={voice_id}", env)
else:
    env += f"\n{field}={voice_id}\n"

with open(env_path, "w") as f:
    f.write(env)

print(f"✅ Saved to backend/.env")
print(f"\n🔄 Now regenerating all stories in {label}'s voice...")

# Re-run enrich_stories.py
os.environ["ELEVENLABS_API_KEY"] = API_KEY
os.environ["ELEVENLABS_VOICE_ID"] = voice_id
os.environ["MONGODB_URL"] = os.getenv("MONGODB_URL", "mongodb://localhost:27017")
os.environ["DATABASE_NAME"] = os.getenv("DATABASE_NAME", "bedtime_storyteller")
os.environ["BASE_URL"] = os.getenv("BASE_URL", "http://10.100.1.95:8000")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY", "")

exec(open("backend/enrich_stories.py").read())
