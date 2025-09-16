import io
import os
import streamlit as st
from dotenv import load_dotenv

from services.stt_deepgram import transcribe_audio
from services.llm_gemini import generate_reply
from services.tts_cartesia import synthesize_mp3, list_voices

load_dotenv()

st.set_page_config(page_title="Voice Assistant (Deepgram → Gemini → Cartesia)")
st.title("🎙️ Voice Assistant")
st.caption("STT: Deepgram • LLM: Gemini • TTS: Cartesia")

# --- Sidebar: keys & options (just status, not the secrets) ---
with st.sidebar:
    st.subheader("Config")
    st.write("Deepgram key:", "✅ set" if os.getenv("DEEPGRAM_API_KEY") else "❌ missing")
    st.write("Gemini key:", "✅ set" if os.getenv("GEMINI_API_KEY") else "❌ missing")
    st.write("Cartesia key:", "✅ set" if os.getenv("CARTESIA_API_KEY") else "❌ missing")
    st.divider()
    language = st.selectbox("Language (STT/TTS)", ["en", "es", "hi", "fr", "de"], index=0, key="language_select")
    system_style = st.text_input("System style", "You are a concise, helpful assistant.")

# --- Voices dropdown (fetched from API) ---
@st.cache_data(ttl=600)
def _fetch_voices(api_key: str, version: str):
    try:
        data = list_voices(api_key=api_key, cartesia_version=version)
        voices = data.get("data", [])
        return {f"{v.get('name','(unnamed)')} ({v.get('language','?')})": v["id"] for v in voices}
    except Exception as e:
        st.warning(f"Could not fetch Cartesia voices: {e}")
        return {}

CARTESIA_API_KEY = os.getenv("CARTESIA_API_KEY", "")
CARTESIA_VERSION = os.getenv("CARTESIA_VERSION", "2025-04-16")

voice_map = _fetch_voices(CARTESIA_API_KEY, CARTESIA_VERSION)
default_voice_id = os.getenv("CARTESIA_VOICE_ID", "")

# Find label for default voice (if present)
labels = list(voice_map.keys()) or ["(no voices found)"]
default_label = next((lbl for lbl, vid in voice_map.items() if vid == default_voice_id), None)

voice_label = st.selectbox(
    "Cartesia voice",
    labels,
    index=(labels.index(default_label) if default_label in labels else 0),
    key="cartesia_voice_select"
)
voice_id = voice_map.get(voice_label, default_voice_id)

if not voice_id:
    st.warning("No voice selected and CARTESIA_VOICE_ID is empty. Select a voice from the dropdown.")

# --- Audio input + action buttons ---
audio = st.audio_input("Hold to record (or click to start/stop)")
cols = st.columns(2)
go = cols[0].button("Transcribe → Think → Speak", type="primary", disabled=audio is None)
audition = cols[1].button("🔊 Audition selected voice", disabled=not voice_id)

# --- Audition flow ---
if audition and voice_id:
    try:
        mp3 = synthesize_mp3("Hi! This is a quick voice check.", voice_id=voice_id, language=language)
        st.audio(io.BytesIO(mp3), format="audio/mp3")
    except Exception as e:
        st.error(f"TTS audition failed: {e}")

# --- Main flow ---
if go:
    if audio is None:
        st.stop()

    # 1) STT
    with st.spinner("Transcribing…"):
        try:
            mime = getattr(audio, "type", None) or "audio/wav"  # browser often gives audio/webm
            user_text = transcribe_audio(audio.getvalue(), content_type=mime, language=language)
        except Exception as e:
            st.error(f"STT failed: {e}")
            st.stop()

    st.write("**You said:**", user_text if user_text else "_(no words detected)_")

    # 2) LLM
    with st.spinner("Thinking with Gemini…"):
        try:
            reply = generate_reply(user_text, system_style=system_style)
        except Exception as e:
            st.error(f"LLM failed: {e}")
            st.stop()

    st.write("**Assistant:**", reply)

    # 3) TTS
    with st.spinner("Synthesizing speech…"):
        try:
            if not voice_id:
                raise RuntimeError("Missing voice_id. Choose a voice from the dropdown.")
            mp3 = synthesize_mp3(reply, voice_id=voice_id, language=language)
        except Exception as e:
            st.error(f"TTS failed: {e}")
            st.stop()

    st.audio(io.BytesIO(mp3), format="audio/mp3")
    st.download_button("Download reply.mp3", data=mp3, file_name="reply.mp3", mime="audio/mpeg")
