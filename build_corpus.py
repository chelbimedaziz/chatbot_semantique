import wikipedia
import json

wikipedia.set_lang("en")

topics = [
    "Artificial intelligence", "Machine learning", "Deep learning",
    "Artificial neural network", "Natural language processing",
    "Computer vision", "Reinforcement learning", "Data science",
    "Supervised learning", "Unsupervised learning",
    "Generative artificial intelligence", "Large language model",
    "ChatGPT", "Transformer (machine learning model)", "Gradient descent",
    "Backpropagation", "Convolutional neural network", "Recurrent neural network",
    "Support vector machine", "Decision tree learning", "Random forest",
    "K-means clustering", "Principal component analysis",
    "Artificial general intelligence", "Explainable AI",
    "Federated learning", "Transfer learning", "Feature engineering",
    "Model evaluation", "Hyperparameter optimization"
]

corpus = []
for topic in topics:
    try:
        page = wikipedia.page(topic, auto_suggest=False)  #  évite les redirections inattendues
        text = page.content[:5000]
        sentences = [s.strip() for s in text.split(". ") if len(s.strip()) > 20]  #  filtre les phrases trop courtes
        corpus.extend(sentences)
        print(f" Collected: {topic} ({len(sentences)} sentences)")
    except Exception as e:
        print(f" Error with '{topic}': {e}")

corpus = list(set(corpus))  # remove duplicates

with open("corpus.json", "w", encoding="utf-8") as f:
    json.dump(corpus, f, indent=4, ensure_ascii=False)  #  ensure_ascii=False pour les caractères spéciaux

print(f"\nFinal corpus size: {len(corpus)} sentences")