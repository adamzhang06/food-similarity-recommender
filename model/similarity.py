from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Function to find the top_k most similar embeddings to a given query embedding
def find_similar(query_embedding, all_embeddings, top_k=5):
    sims = cosine_similarity([query_embedding], all_embeddings)[0]
    indices = np.argsort(sims)[-top_k:][::-1]
    return indices
