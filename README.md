# Voice AI Demo

A small toolkit for voice cloning and batch text-to-speech generation, built on top of a commercial TTS API (ElevenLabs-style REST interface). Demonstrates the core workflow used to produce narrated video content: clone or select a voice, then batch-generate audio for a full script broken into scenes.

## Problem

Producing narrated AI video content at volume means generating dozens of short audio clips per project, each tied to a specific scene/shot, with consistent voice, pacing, and naming so the audio can be dropped straight into an editing timeline. Doing this by hand through a web UI doesn't scale.

## How it works

1. **Voice setup**: clone a voice from a short reference sample, or select an existing voice ID from the provider's library.
2. **Script segmentation**: a script is broken into scene-labeled lines (`scene_01`, `scene_02`, ...) so each generated clip maps directly to a shot in the edit.
3. **Batch generation**: each line is sent to the TTS API with consistent voice settings (stability, similarity, style), and the resulting audio is saved with a filename matching its scene ID.
4. **Manifest output**: a JSON manifest listing scene ID, script text, and output file path is written alongside the audio, so the pipeline can be chained directly into a video assembly step.

## Structure

```
voice_client.py     # Thin API client: clone voice, generate speech
batch_generate.py   # Script segmentation + batch generation + manifest output
scripts/example.txt # Example scene-labeled script
```

## Example

```python
from voice_client import VoiceClient
from batch_generate import generate_from_script

client = VoiceClient(api_key="YOUR_API_KEY")
voice_id = client.list_voices()[0]["voice_id"]

manifest = generate_from_script(
    client,
    script_path="scripts/example.txt",
    voice_id=voice_id,
    output_dir="output/",
)
print(manifest)
```

## Stack

- Python 3.11
- `requests` (REST API client)
- Any ElevenLabs-compatible TTS/voice cloning API

## Notes

This is a generalized personal demo of a voice generation workflow, not tied to any specific client project. Swap `BASE_URL` in `voice_client.py` to point at whichever provider's API you're using.
