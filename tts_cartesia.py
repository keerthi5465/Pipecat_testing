# services/tts_cartesia.py
import os
import json
import requests
from dotenv import load_dotenv
load_dotenv()

def _env(key: str, default: str | None = None) -> str | None:
    return os.getenv(key, default)

def list_voices(api_key: str | None = None, cartesia_version: str | None = None, page: str | None = None) -> dict:
    """
    Returns dict with keys: data (list of voices), next_page, has_more
    """
    api_key = api_key or _env("CARTESIA_API_KEY")
    if not api_key:
        raise RuntimeError("CARTESIA_API_KEY is missing")

    version = cartesia_version or _env("CARTESIA_VERSION", "2025-04-16")
    url = "https://api.cartesia.ai/voices"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Cartesia-Version": version,
    }
    params = {}
    if page:
        params["page"] = page

    r = requests.get(url, headers=headers, params=params, timeout=30)
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(f"Cartesia voices HTTP {r.status_code}: {r.text[:500]}") from e

    return r.json()

def synthesize_mp3(
    text: str,
    voice_id: str | None = None,
    model_id: str | None = None,
    language: str | None = None,
    bitrate: int = 128000,
    sample_rate: int = 44100,
    api_key: str | None = None,
    cartesia_version: str | None = None,
) -> bytes:
    """
    Calls /tts/bytes and returns MP3 bytes.
    """
    api_key = api_key or _env("CARTESIA_API_KEY")
    if not api_key:
        raise RuntimeError("CARTESIA_API_KEY is missing")

    version = cartesia_version or _env("CARTESIA_VERSION", "2025-04-16")
    model_id = model_id or _env("CARTESIA_MODEL_ID", "sonic-2")
    language = language or _env("CARTESIA_LANGUAGE", "en")
    voice_id = voice_id or _env("CARTESIA_VOICE_ID", "")

    if not voice_id:
        raise RuntimeError("No voice_id provided and CARTESIA_VOICE_ID is empty")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Cartesia-Version": version,
        "Content-Type": "application/json",
    }
    body = {
        "model_id": model_id,
        "transcript": text,
        "voice": {"mode": "id", "id": voice_id},
        "language": language,
        "output_format": {
            "container": "mp3",
            "bit_rate": bitrate,
            "sample_rate": sample_rate
        },
    }
    r = requests.post("https://api.cartesia.ai/tts/bytes", headers=headers, data=json.dumps(body), timeout=120)
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(f"Cartesia TTS HTTP {r.status_code}: {r.text[:500]}") from e

    return r.content
