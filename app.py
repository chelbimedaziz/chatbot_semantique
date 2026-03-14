import streamlit as st
from textblob import TextBlob
from chatbot import answer_question
import re

st.set_page_config(page_title="AI Knowledge Chatbot", page_icon="🤖", layout="centered")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29, #302b63, #24243e);
        color: white;
    }
    .main-title {
        text-align: center;
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(90deg, #a78bfa, #60a5fa, #34d399);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem;
    }
    .subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 1rem;
        margin-bottom: 2rem;
    }
    .user-bubble {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        padding: 12px 18px;
        border-radius: 18px 18px 4px 18px;
        margin: 8px 0 8px auto;
        max-width: 75%;
        width: fit-content;
        margin-left: auto;
        font-size: 0.95rem;
        box-shadow: 0 4px 15px rgba(99, 102, 241, 0.3);
    }
    .bot-bubble {
        background: linear-gradient(135deg, #1e293b, #334155);
        color: #e2e8f0;
        padding: 12px 18px;
        border-radius: 18px 18px 18px 4px;
        margin: 8px auto 8px 0;
        max-width: 75%;
        width: fit-content;
        font-size: 0.95rem;
        border-left: 3px solid #60a5fa;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }
    .correction-tag {
        background: rgba(251, 191, 36, 0.15);
        border: 1px solid #fbbf24;
        color: #fbbf24;
        border-radius: 8px;
        padding: 4px 10px;
        font-size: 0.78rem;
        margin-bottom: 4px;
        width: fit-content;
    }
    .bubble-label { font-size: 0.72rem; color: #64748b; margin-bottom: 2px; }
    .stTextInput > div > div > input {
        background-color: #1e293b !important;
        color: white !important;
        border: 2px solid #4f46e5 !important;
        border-radius: 12px !important;
        padding: 12px 16px !important;
        font-size: 1rem !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #818cf8 !important;
        box-shadow: 0 0 0 3px rgba(129, 140, 248, 0.2) !important;
    }
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6) !important;
        color: white !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
        width: 100%;
    }
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4) !important;
    }
    hr { border-color: #334155 !important; }
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────
st.markdown('<div class="main-title">🤖 AI Knowledge Chatbot</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Ask me anything about Artificial Intelligence</div>', unsafe_allow_html=True)
st.markdown("---")

# ── Session state ─────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "bot", "text": "Hello! 👋 I'm your AI assistant. Ask me anything about ML, Deep Learning, NLP and more!", "corrected": None}
    ]

# ── Chat history ──────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f'<div class="bubble-label" style="text-align:right">You</div><div class="user-bubble">{msg["text"]}</div>', unsafe_allow_html=True)
    else:
        # ✅ Show correction notice if spelling was fixed
        if msg.get("corrected"):
            st.markdown(f'<div class="correction-tag">✏️ Did you mean: <b>{msg["corrected"]}</b>?</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="bubble-label">🤖 Bot</div><div class="bot-bubble">{msg["text"]}</div>', unsafe_allow_html=True)

# ── Input ─────────────────────────────────────────────────────
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input("", placeholder="Type your question here...", label_visibility="collapsed", key="input")
with col2:
    send = st.button("Send ➤")

# ── Handle send ───────────────────────────────────────────────
if send and user_input.strip():
    # Detect spelling correction
    from textblob import TextBlob
    corrected = str(TextBlob(user_input).correct())
    was_corrected = corrected.lower() != user_input.lower()

    st.session_state.messages.append({"role": "user", "text": user_input, "corrected": None})

    with st.spinner("Thinking..."):
        response = answer_question(user_input)

    st.session_state.messages.append({
        "role": "bot",
        "text": response,
        "corrected": corrected if was_corrected else None  # ✅ show yellow tag if typo
    })
    st.rerun()

# ── Footer ────────────────────────────────────────────────────
st.markdown("---")
st.markdown('<p style="text-align:center; color:#475569; font-size:0.8rem;">Powered by SentenceTransformers & Wikipedia 🚀</p>', unsafe_allow_html=True)