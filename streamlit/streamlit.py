from __future__ import annotations

import sys
import base64
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# PATH SETUP
ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.append(str(SCRIPTS))

load_dotenv(ROOT / ".env")


from embedding import EmbeddingModel
from llm_wrapper import generate_answer, DEFAULT_LLM_MODEL
from vector import FaissVectorStore

try:
    from voice import TextToSpeech, SpeechToText, VOICE_OPTIONS, DEFAULT_VOICE, HAS_EDGE_TTS, HAS_WHISPER
except ImportError:
    HAS_EDGE_TTS = False
    HAS_WHISPER = False
    VOICE_OPTIONS = {}
    DEFAULT_VOICE = None

try:
    from audio_recorder_streamlit import audio_recorder
    HAS_AUDIO_RECORDER = True
except ImportError:
    HAS_AUDIO_RECORDER = False


st.set_page_config(
    page_title="Nyaya.exe",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

TOP_K = 8
LOGO_PATH = ROOT / "assets" / "images" / "logo.jpeg"

SUGGESTIONS = [
    ("What are fundamental rights in Nepal's constitution?", 
     "What are the fundamental rights guaranteed by the Constitution of Nepal?"),
    ("How is citizenship acquired in Nepal?", 
     "How can someone acquire Nepali citizenship?"),
    ("What are employee rights in civil service?", 
     "What are the rights and benefits of civil service employees in Nepal?"),
    ("What are privacy laws in Nepal?", 
     "What does Nepal's Individual Privacy Act protect?"),
]


def get_logo_base64() -> str | None:
    if LOGO_PATH.exists():
        return base64.b64encode(LOGO_PATH.read_bytes()).decode()
    return None


def load_css() -> str:
    css_file = Path(__file__).parent / "style.css"
    if css_file.exists():
        return f"<style>{css_file.read_text()}</style>"
    return ""


@st.cache_resource(show_spinner=False)
def load_resources():
    
    model = EmbeddingModel()
    store = FaissVectorStore()
    index_path = ROOT / "database" / "legal_faiss.index"
    
    if index_path.exists():
        store.load()
    else:
        store.build(processed_dir=ROOT / "dataset" / "processed", embedding_model=model)
    
    return model, store


@st.cache_resource(show_spinner=False)
def load_tts():
    return TextToSpeech() if HAS_EDGE_TTS else None


@st.cache_resource(show_spinner=False)
def load_stt():
    return SpeechToText() if HAS_WHISPER else None


def search_and_answer(question: str, model, store) -> tuple[str, str]:
    hits = store.search(question, embedding_model=model, top_k=TOP_K)
    
    # Build sources text
    sources_lines = []
    for i, hit in enumerate(hits, 1):
        meta = hit.get("metadata", {})
        source = meta.get("filename", meta.get("title", "Unknown"))
        year = meta.get("year", "")
        preview = hit["text"][:400] + "..." if len(hit["text"]) > 400 else hit["text"]
        sources_lines.append(f"**{i}. {source}** ({year})\n> {preview}")
    
    sources_text = "\n\n".join(sources_lines)
    
    try:
        context = [h["text"] for h in hits]
        answer = generate_answer(question, context, model=DEFAULT_LLM_MODEL)
        return answer, sources_text
    except Exception as e:
        return f" Error generating response: {e}", sources_text


def generate_tts_audio(text: str, voice: str | None = None) -> bytes | None:
    tts = load_tts()
    if tts:
        tts.set_voice(voice or DEFAULT_VOICE)
        return tts.synthesize(text)
    return None


def transcribe_audio(audio_bytes: bytes) -> str:
    stt = load_stt()
    return stt.transcribe(audio_bytes) if stt else ""


def process_query(prompt: str, is_voice: bool = False) -> None:
    # Add user message
    display_prompt = f"🎤 {prompt}" if is_voice else prompt
    st.session_state.messages.append({"role": "user", "content": display_prompt})
    
    with st.chat_message("user", avatar="👤"):
        st.markdown(display_prompt)
    
    # Generate response
    with st.chat_message("assistant", avatar="⚖️"):
        with st.spinner(""):
            answer, sources = search_and_answer(prompt, model, store)
        
        st.markdown(answer)
        with st.expander("📚 View Sources"):
            st.markdown(sources)
        
        # Generate TTS 
        audio_data = None
        should_speak = is_voice or st.session_state.tts_enabled
        
        if should_speak and HAS_EDGE_TTS:
            with st.spinner("🔊 Generating audio..."):
                try:
                    voice = st.session_state.selected_voice or DEFAULT_VOICE
                    audio_data = generate_tts_audio(answer, voice)
                    if audio_data:
                        st.audio(audio_data, format="audio/mp3", autoplay=True)
                except Exception as e:
                    st.caption(f" TTS error: {e}")
    
    # Save to history
    st.session_state.messages.append({
        "role": "assistant", 
        "content": answer, 
        "sources": sources, 
        "audio": audio_data
    })


DEFAULTS = {
    "messages": [],
    "tts_enabled": False,
    "selected_voice": DEFAULT_VOICE if HAS_EDGE_TTS else None,
    "stt_text": "",
    "last_audio_hash": None,
    "suggestion": None,
}

for key, default in DEFAULTS.items():
    if key not in st.session_state:
        st.session_state[key] = default


LOGO_BASE64 = get_logo_base64()
st.markdown(load_css(), unsafe_allow_html=True)

# Load resources
try:
    model, store = load_resources()
except Exception as e:
    st.error(f"Failed to load resources: {e}")
    st.stop()

with st.sidebar:
    st.title("⚖️ Nyaya.exe")
    
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    # TTS Settings
    st.subheader("🔊 Text-to-Speech")
    if HAS_EDGE_TTS:
        st.session_state.tts_enabled = st.toggle(
            "Enable TTS", 
            value=st.session_state.tts_enabled
        )
        if st.session_state.tts_enabled:
            voice_name = st.selectbox("Voice", options=list(VOICE_OPTIONS.keys()))
            st.session_state.selected_voice = VOICE_OPTIONS[voice_name]
    else:
        st.caption("⚠️ Install: `pip install edge-tts`")
    
    st.divider()
    
    # STT Settings
    st.subheader("🎤 Voice Input")
    if HAS_WHISPER and HAS_AUDIO_RECORDER:
        st.caption("Click mic → Speak → Wait")
        audio_bytes = audio_recorder(
            text="",
            recording_color="#ff6b6b",
            neutral_color="#d4a574",
            icon_name="microphone",
            icon_size="2x",
            pause_threshold=2.0,
            sample_rate=16000,
            key="voice_recorder"
        )
        
        if audio_bytes:
            audio_hash = hash(audio_bytes)
            if audio_hash != st.session_state.last_audio_hash:
                st.session_state.last_audio_hash = audio_hash
                with st.spinner("🎤 Transcribing..."):
                    try:
                        text = transcribe_audio(audio_bytes)
                        if text and not text.startswith("[Error"):
                            st.success(f'✓ "{text}"')
                            st.session_state.stt_text = text
                        else:
                            st.warning(text or "No speech detected")
                    except Exception as e:
                        st.error(f"STT Error: {e}")
    elif HAS_WHISPER:
        st.caption("⚠️ Install: `pip install audio-recorder-streamlit`")
    else:
        st.caption("⚠️ Install: `pip install SpeechRecognition`")
    
    st.divider()
    st.caption("Powered by RAG technology")
    st.caption("Built for Nepal Legal Documents")



# Welcome screen 
if not st.session_state.messages:
    logo_html = f'<img src="data:image/jpeg;base64,{LOGO_BASE64}" class="logo-img">' if LOGO_BASE64 else ""
    st.markdown(f"""
        <div class="welcome-container">
            {logo_html}
            <div class="welcome-title">Nyaya.exe</div>
            <div class="welcome-subtitle">Ask questions about Nepali laws and legal documents</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Suggestion buttons
    cols = st.columns(2)
    for i, (button_text, query) in enumerate(SUGGESTIONS):
        with cols[i % 2]:
            if st.button(f" {button_text}", use_container_width=True, key=f"sug{i}"):
                st.session_state.suggestion = query
                st.rerun()

# Display chat history
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "⚖️"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])
        if msg["role"] == "assistant":
            if "sources" in msg:
                with st.expander("📚 View Sources"):
                    st.markdown(msg["sources"])
            if msg.get("audio"):
                st.audio(msg["audio"], format="audio/mp3")



# Handle suggestion click
if st.session_state.suggestion:
    prompt = st.session_state.suggestion
    st.session_state.suggestion = None
    process_query(prompt)

# Handle voice input
if st.session_state.stt_text:
    prompt = st.session_state.stt_text
    st.session_state.stt_text = ""
    st.session_state.last_audio_hash = None
    process_query(prompt, is_voice=True)

# Handle text input
if prompt := st.chat_input("Ask about Nepali laws..."):
    process_query(prompt)
