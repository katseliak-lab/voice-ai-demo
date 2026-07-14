import requests

BASE_URL = "https://api.elevenlabs.io/v1"


class VoiceClient:
    def __init__(self, api_key: str, base_url: str = BASE_URL):
        self.api_key = api_key
        self.base_url = base_url

    def _headers(self, json_body: bool = True) -> dict:
        headers = {"xi-api-key": self.api_key}
        if json_body:
            headers["Content-Type"] = "application/json"
        return headers

    def list_voices(self) -> list:
        resp = requests.get(f"{self.base_url}/voices", headers=self._headers(json_body=False), timeout=30)
        resp.raise_for_status()
        return resp.json().get("voices", [])

    def clone_voice(self, name: str, sample_paths: list, description: str = "") -> str:
        """Clones a voice from one or more reference audio samples, returns the new voice_id."""
        files = [("files", open(p, "rb")) for p in sample_paths]
        data = {"name": name, "description": description}
        resp = requests.post(
            f"{self.base_url}/voices/add",
            headers=self._headers(json_body=False),
            data=data,
            files=files,
            timeout=60,
        )
        for _, f in files:
            f.close()
        resp.raise_for_status()
        return resp.json()["voice_id"]

    def generate_speech(self, text: str, voice_id: str, stability: float = 0.5, similarity_boost: float = 0.75) -> bytes:
        """Generates speech audio (bytes, mp3) for a single line of text."""
        payload = {
            "text": text,
            "voice_settings": {
                "stability": stability,
                "similarity_boost": similarity_boost,
            },
        }
        resp = requests.post(
            f"{self.base_url}/text-to-speech/{voice_id}",
            headers=self._headers(),
            json=payload,
            timeout=60,
        )
        resp.raise_for_status()
        return resp.content
