from sentence_transformers import SentenceTransformer

# Function to embed a list of texts using the all-MiniLM-L6-v2 SentenceTransformer model
def embed_texts(texts, model_name="all-MiniLM-L6-v2"):
    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=True)
    return embeddings
