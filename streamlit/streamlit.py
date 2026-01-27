
from __future__ import annotations

import sys
import base64
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Ensure we can import from scripts/
ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.append(str(SCRIPTS))

# Load .env
load_dotenv(ROOT / ".env")

from embedding import EmbeddingModel, DEFAULT_EMBEDDING_MODEL  
from llm_wrapper import generate_answer, DEFAULT_LLM_MODEL  
from vector import FaissVectorStore  

# Page config
st.set_page_config(
    page_title="Nyaya.exe",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load logo as base64
LOGO_PATH = ROOT / "assets" / "images" / "logo.jpeg"
def get_logo_base64():
    if LOGO_PATH.exists():
        with open(LOGO_PATH, "rb") as f:
            return base64.b64encode(f.read()).decode()
    return None

LOGO_BASE64 = get_logo_base64()

# Load CSS from external file
def load_css():
    css_file = Path(__file__).parent / "style.css"
    if css_file.exists():
        with open(css_file) as f:
            return f"<style>{f.read()}</style>"
    return ""

st.markdown(load_css(), unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "resources_loaded" not in st.session_state:
    st.session_state.resources_loaded = False
if "model" not in st.session_state:
    st.session_state.model = None
if "store" not in st.session_state:
    st.session_state.store = None


@st.cache_resource(show_spinner=False)
def load_resources():
    """Load embedding model and FAISS store."""
    model = EmbeddingModel()
    store = FaissVectorStore()
    index_path = ROOT / "database" / "legal_faiss.index"
    
    if index_path.exists():
        store.load()
    else:
        store.build(processed_dir=ROOT / "dataset" / "processed", embedding_model=model)
    
    return model, store


def search_and_answer(question: str, model, store, top_k: int, use_llm: bool, llm_model: str):
    """Search FAISS and optionally generate LLM answer. Returns (answer, sources_text)."""
    hits = store.search(question, embedding_model=model, top_k=top_k)
    
    # Build sources text
    sources_text = ""
    for i, hit in enumerate(hits, 1):
        meta = hit.get("metadata", {})
        source = meta.get("filename", meta.get("title", "Unknown"))
        year = meta.get("year", "")
        text_preview = hit["text"][:400] + "..." if len(hit["text"]) > 400 else hit["text"]
        sources_text += f"\n\n**{i}. {source}** ({year})\n> {text_preview}"
    
    if use_llm:
        try:
            context = [h["text"] for h in hits]
            answer = generate_answer(question, context, model=llm_model)
            return answer, sources_text
        except Exception as e:
            return f"⚠️ Error generating response: {e}", sources_text
    else:
        return "Here are the relevant sources I found:", sources_text


# Default settings
top_k = 8
use_llm = True
llm_model = DEFAULT_LLM_MODEL

# Sidebar
with st.sidebar:
    st.title("⚖️ Nyaya.exe")
    
    if st.button("➕ New Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    
    st.caption("Powered by RAG technology")
    st.caption("Built for Nepal Legal Documents")

# Load resources silently
try:
    model, store = load_resources()
    resources_ready = True
except Exception as e:
    st.error(f"Failed to load resources: {e}")
    resources_ready = False
    st.stop()

# Main chat area
if not st.session_state.messages:
    # Welcome screen with logo
    logo_html = f'<img src="data:image/jpeg;base64,{LOGO_BASE64}" class="logo-img">' if LOGO_BASE64 else ""
    
    st.markdown(f"""
        <div class="welcome-container">
            {logo_html}
            <div class="welcome-title">Nyaya.exe</div>
            <div class="welcome-subtitle">Ask questions about Nepali laws and legal documents</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Suggestion cards
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button(" What are fundamental rights in Nepal's constitution?", use_container_width=True, key="sug1"):
            st.session_state.suggestion = "What are the fundamental rights guaranteed by the Constitution of Nepal?"
            st.rerun()
        
        if st.button(" How is citizenship acquired in Nepal?", use_container_width=True, key="sug2"):
            st.session_state.suggestion = "How can someone acquire Nepali citizenship?"
            st.rerun()
    
    with col2:
        if st.button(" What are employee rights in civil service?", use_container_width=True, key="sug3"):
            st.session_state.suggestion = "What are the rights and benefits of civil service employees in Nepal?"
            st.rerun()
        
        if st.button(" What are privacy laws in Nepal?", use_container_width=True, key="sug4"):
            st.session_state.suggestion = "What does Nepal's Individual Privacy Act protect?"
            st.rerun()

# Display chat history
for message in st.session_state.messages:
    avatar = "👤" if message["role"] == "user" else "⚖️"
    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])
        if message["role"] == "assistant" and "sources" in message:
            with st.expander("📚 View Sources"):
                st.markdown(message["sources"])

# Handle suggestion click
if "suggestion" in st.session_state and st.session_state.suggestion:
    prompt = st.session_state.suggestion
    st.session_state.suggestion = None
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="⚖️"):
        with st.spinner(""):
            answer, sources = search_and_answer(
                prompt, 
                model, 
                store, 
                top_k=top_k, 
                use_llm=use_llm, 
                llm_model=llm_model
            )
        st.markdown(answer)
        with st.expander("📚 View Sources"):
            st.markdown(sources)
    
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})

# Chat input
if prompt := st.chat_input("Ask about Nepali laws..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)
    
    with st.chat_message("assistant", avatar="⚖️"):
        with st.spinner(""):
            answer, sources = search_and_answer(
                prompt, 
                model, 
                store, 
                top_k=top_k, 
                use_llm=use_llm, 
                llm_model=llm_model
            )
        st.markdown(answer)
        with st.expander("📚 View Sources"):
            st.markdown(sources)
    
    st.session_state.messages.append({"role": "assistant", "content": answer, "sources": sources})
