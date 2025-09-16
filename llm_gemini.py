
import os
import requests
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

def generate_reply(user_text: str, system_style: str = "You are a concise, helpful assistant.") -> str:
    """
    Calls Gemini via REST and returns plain text.
    """
    if not GEMINI_API_KEY:
        raise RuntimeError("GEMINI_API_KEY is missing")

    payload = {
        "contents": [
            {"role": "user", "parts": [{"text": f"{system_style}\nUser: {user_text}"}]}
        ]
    }
    r = requests.post(
        GEMINI_URL,
        params={"key": GEMINI_API_KEY},
        json=payload,
        timeout=60,
    )
    try:
        r.raise_for_status()
    except requests.HTTPError as e:
        raise RuntimeError(f"Gemini HTTP {r.status_code}: {r.text[:500]}") from e

    j = r.json()
    try:
        return "".join(
            p.get("text", "")
            for c in j.get("candidates", [])
            for p in c.get("content", {}).get("parts", [])
        ).strip() or "Sorry, I couldn't generate a response."
    except Exception:
        return "Sorry, I couldn't generate a response."
