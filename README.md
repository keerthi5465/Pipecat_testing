# 🎙️ Voice Pipeline (Deepgram → Gemini → Cartesia)

This project is a simple **voice assistant web app** built with **Streamlit** in Python.  
It lets you record audio in the browser, transcribe it with **Deepgram (STT)**, generate a reply using **Gemini (LLM)**, and then synthesize speech with **Cartesia (TTS)**.

---

## 🚀 Features
- 🎤 **Record audio** directly in the browser via Streamlit’s `st.audio_input`.
- 📝 **Speech-to-text** using Deepgram (`nova-3` model).
- 🤖 **LLM responses** from Google’s Gemini (`gemini-2.5-flash`).
- 🔊 **Text-to-speech** with Cartesia (`sonic-2` model).
- 🎚️ **Voice selector**: fetch and audition Cartesia voices dynamically.
- 🌐 Multi-language support (English, Spanish, Hindi, French, German).
- 🖥️ Simple Streamlit UI for quick prototyping.

---

## 📦 Project Structure
```
voice-pipeline/
│
├── app.py                    # Streamlit frontend
│── stt_deepgram.py        # Deepgram STT helper
│── llm_gemini.py          # Gemini LLM helper
│── tts_cartesia.py        # Cartesia TTS + voices helpers
├── requirements.txt
└── README.md
```

---

## ⚙️ Setup

### 1. Clone & create environment
```bash
git clone <your-repo-url> voice-pipeline
cd voice-pipeline
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure `.env`
Create a `.env` file in the project root:

```ini
# Deepgram
DEEPGRAM_API_KEY=dg_xxx

# Gemini
GEMINI_API_KEY=xxx
GEMINI_MODEL=gemini-2.5-flash

# Cartesia
CARTESIA_API_KEY=sk_live_xxx
CARTESIA_VERSION=2025-04-16
CARTESIA_MODEL_ID=sonic-2
CARTESIA_LANGUAGE=en
CARTESIA_VOICE_ID=694f9389-aac1-45b6-b726-9d9369183238   # Pick from /voices
```

> 🔑 **Where to get API keys:**  
> - [Deepgram Console](https://console.deepgram.com/) → API Keys  
> - [Google AI Studio](https://aistudio.google.com/) → Gemini API Key  
> - [Cartesia Dashboard](https://cartesia.ai/) → API Key & Voices (`GET /voices`)

---

## ▶️ Run the app
```bash
streamlit run app.py
```

Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## 🛠️ Usage
1. Pick a **language** and **voice** from the sidebar.
2. Record audio using the mic widget.
3. Click **Transcribe → Think → Speak**:
   - Your speech is transcribed (Deepgram).
   - A reply is generated (Gemini).
   - The reply is spoken (Cartesia).
4. Listen to the assistant’s response or download the `.mp3`.

You can also audition voices with the **🔊 Audition selected voice** button.

---

## 📂 Requirements
- Python 3.10+
- [Deepgram account](https://console.deepgram.com/)
- [Google Gemini API key](https://aistudio.google.com/)
- [Cartesia account](https://cartesia.ai/)

