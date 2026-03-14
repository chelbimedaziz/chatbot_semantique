from sentence_transformers import SentenceTransformer  #  imports séparés
from preprocess import load_corpus
import numpy as np

print("Loading transformer model...")
model = SentenceTransformer("all-mpnet-base-v2")

corpus, clean_corpus = load_corpus()

print("Creating embeddings...")
corpus_vectors = model.encode(clean_corpus, show_progress_bar=True, batch_size=64)  #  batch_size pour la performance

np.save("vectors.npy", corpus_vectors)
print(f" Embeddings created: {corpus_vectors.shape}")