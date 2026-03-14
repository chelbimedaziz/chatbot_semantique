import json
import spacy

nlp = spacy.load("en_core_web_sm")

def clean_text(text):
    doc = nlp(text.lower())
    tokens = [
        token.lemma_ for token in doc
        if not token.is_stop and not token.is_punct and token.is_alpha
    ]
    return " ".join(tokens)

def load_corpus():
    with open("corpus.json", "r", encoding="utf-8") as f:
        corpus = json.load(f)
    print("Cleaning corpus...")
    clean_corpus = [clean_text(sent) for sent in corpus]
    return corpus, clean_corpus