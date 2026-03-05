#!/usr/bin/env python3
"""Record your voice from the Mac microphone and save as voice_recording.wav"""

import sounddevice as sd
import soundfile as sf
import numpy as np

DURATION = 120   # seconds (2 minutes — press Ctrl+C to stop early)
SAMPLE_RATE = 44100
OUTPUT_FILE = "voice_recording.wav"

print("🎙 Voice Recorder")
print("=" * 40)
print(f"Recording for up to {DURATION} seconds...")
print("Press Ctrl+C to stop early and save.\n")
print("Speak naturally — read a story, describe your day, anything!")
print("Recording starts NOW...\n")

frames = []

def callback(indata, frame_count, time_info, status):
    frames.append(indata.copy())

try:
    with sd.InputStream(samplerate=SAMPLE_RATE, channels=1, dtype='float32', callback=callback):
        elapsed = 0
        while elapsed < DURATION:
            sd.sleep(1000)
            elapsed += 1
            remaining = DURATION - elapsed
            bar = "█" * (elapsed // 5) + "░" * (remaining // 5)
            print(f"\r  [{bar}] {elapsed}s / {DURATION}s", end="", flush=True)
except KeyboardInterrupt:
    print("\n\nStopped early.")

print(f"\n\n✅ Saving to {OUTPUT_FILE}...")
audio = np.concatenate(frames, axis=0)
sf.write(OUTPUT_FILE, audio, SAMPLE_RATE)
print(f"✅ Saved! File size: {len(audio)/SAMPLE_RATE:.1f} seconds of audio")
print(f"\nNow upload {OUTPUT_FILE} in the app:")
print("  Parent Dashboard → Manage Voices → Upload File")
