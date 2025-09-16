# services/stt_deepgram.py
import os
import requests
from dotenv import load_dotenv
load_dotenv()
DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
DEEPGRAM_URL = "https://api.deepgram.com/v1/listen"

def transcribe_audio(audio_bytes: bytes, content_type: str = "audio/wav", language: str = "en") -> str:
    """
    Sends recorded audio bytes to Deepgram prerecorded endpoint and returns transcript.
    Use the correct content_type from the browser (e.g., 'audio/webm', 'audio/wav').
    """
    if not DEEPGRAM_API_KEY:
        raise RuntimeError("DEEPGRAM_API_KEY is missing")

    params = {
        "model": "nova-3",
        "smart_format": "true",
        "punctuate": "true",
        # Optionally force language or enable detection:
        # "language": language,
        # "detect_language": "true",
    }

    headers = {
        "Authorization": f"Token {DEEPGRAM_API_KEY}",
        "Content-Type": content_type,
    }

    r = requests.post(DEEPGRAM_URL, params=params, headers=headers, data=audio_bytes, timeout=60)
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(f"Deepgram STT HTTP {r.status_code}: {r.text[:500]}") from e

    j = r.json()
    try:
        return j["results"]["channels"][0]["alternatives"][0]["transcript"].strip()
    except Exception:
        return ""
