import spacy

nlp = spacy.load("en_core_web_sm")

def clean_text(text):

    text = text.lower()

    doc = nlp(text)

    tokens = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct
    ]

    return " ".join(tokens)


def load_corpus():

    with open("corpus.txt", encoding="utf-8") as f:
        raw = f.readlines()

    clean = [clean_text(s) for s in raw]

    return raw, clean