from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import load_corpus, clean_text
from textblob import TextBlob
from rapidfuzz import process, fuzz
import numpy as np
import re

# ── Spell correction ─────────────────────────────────────────
def correct_spelling(text: str) -> str:
    blob = TextBlob(text)
    corrected = str(blob.correct())
    return corrected

# ── Greetings ────────────────────────────────────────────────
GREETINGS = {
    "hello": "Hello! 👋 How can I help you today?",
    "hi": "Hi there! 😊 What would you like to know about AI?",
    "hey": "Hey! 👋 Feel free to ask me anything about Artificial Intelligence!",
    "good morning": "Good morning! ☀️ How can I assist you today?",
    "good afternoon": "Good afternoon! 😊 What can I help you with?",
    "good evening": "Good evening! 🌙 What would you like to know?",
    "how are you": "I'm doing great, thank you for asking! 😄 Ready to answer your AI questions!",
    "what's up": "All good here! 😎 Ask me anything about AI!",
    "whats up": "All good! 😎 What would you like to know about AI?",
    "sup": "Hey! 👋 What can I help you with?",
    "bye": "Goodbye! 👋 It was a pleasure chatting with you!",
    "goodbye": "Goodbye! 👋 Have a great day!",
    "see you": "See you later! 👋 Come back anytime!",
    "thanks": "You're welcome! 😊 Feel free to ask more questions!",
    "thank you": "You're welcome! 😊 Is there anything else I can help you with?",
}

def detect_greeting(text: str):
    text_clean = re.sub(r"[^\w\s]", "", text.lower().strip())

    # ✅ Exact match first
    if text_clean in GREETINGS:
        return GREETINGS[text_clean]

    # ✅ Fuzzy match on greeting keys (handles typos like "helo", "hii", "thaks")
    result = process.extractOne(
        text_clean,
        GREETINGS.keys(),
        scorer=fuzz.ratio,
        score_cutoff=75  # % similarity threshold
    )
    if result:
        matched_key = result[0]
        return GREETINGS[matched_key]

    return None

# ── Load model & corpus ──────────────────────────────────────
print("Loading model and corpus...")
model = SentenceTransformer("all-mpnet-base-v2")
corpus, clean_corpus = load_corpus()
corpus_vectors = np.load("vectors.npy")

# ── Main answer function ─────────────────────────────────────
def answer_question(question: str) -> str:
    # Step 1: correct spelling
    corrected = correct_spelling(question)
    if corrected.lower() != question.lower():
        print(f"[Auto-corrected: '{question}' → '{corrected}']")  # debug log

    # Step 2: check for greeting
    greeting_response = detect_greeting(corrected)
    if greeting_response:
        return greeting_response

    # Step 3: semantic search
    cleaned_q = clean_text(corrected)
    q_vector = model.encode([cleaned_q])
    similarities = cosine_similarity(q_vector, corpus_vectors)[0]
    best_idx = int(np.argmax(similarities))
    score = similarities[best_idx]

    if score < 0.3:
        return "I'm sorry, I don't have enough information about that. Try asking about AI, ML, or Deep Learning!"

    return corpus[best_idx]