import json
import os
from typing import List, Tuple

from voice_client import VoiceClient


def parse_script(script_path: str) -> List[Tuple[str, str]]:
    """
    Parses a scene-labeled script file. Each non-empty line looks like:
        scene_01: Text to be spoken for this scene.
    Returns a list of (scene_id, text) tuples.
    """
    lines = []
    with open(script_path, "r", encoding="utf-8") as f:
        for raw_line in f:
            line = raw_line.strip()
            if not line or ":" not in line:
                continue
            scene_id, text = line.split(":", 1)
            lines.append((scene_id.strip(), text.strip()))
    return lines


def generate_from_script(client: VoiceClient, script_path: str, voice_id: str, output_dir: str) -> dict:
    os.makedirs(output_dir, exist_ok=True)
    lines = parse_script(script_path)

    manifest = {"voice_id": voice_id, "clips": []}

    for scene_id, text in lines:
        audio_bytes = client.generate_speech(text, voice_id=voice_id)
        output_path = os.path.join(output_dir, f"{scene_id}.mp3")
        with open(output_path, "wb") as f:
            f.write(audio_bytes)

        manifest["clips"].append({
            "scene_id": scene_id,
            "text": text,
            "output_path": output_path,
        })

    manifest_path = os.path.join(output_dir, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=2, ensure_ascii=False)

    return manifest
