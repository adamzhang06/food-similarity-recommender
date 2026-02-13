from backend.ingestion.load_data import get_engine
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datasets import Dataset
import numpy as np
import pandas as pd

# ! Settings for embedding
EMBEDDINGS_FILE = "backend/embeddings/recipe_embeddings.npy"
IDS_FILE = "backend/embeddings/recipe_ids.npy"

def generate_and_save_embeddings(embeddings_file=EMBEDDINGS_FILE, ids_file=IDS_FILE):
    engine = get_engine()
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    
    batch_size = 10000  # * Adjust based on memory constraints
    offset = 0
    all_embeddings = []
    all_ids = []
    
    while True:
        query = f"""
        SELECT id, title, directions, ner
        FROM recipes
        ORDER BY id
        LIMIT {batch_size} OFFSET {offset}
        """
        df = pd.read_sql(query, engine)
        
        if df.empty:
            break
        
        texts = [f"{row['title']} {row['directions']} {row['ner']}" for _, row in df.iterrows()]
        embeddings = model.encode(texts, show_progress_bar=True)
        all_embeddings.append(embeddings)
        all_ids.extend(df["id"].tolist())
        offset += batch_size
        
        print(f"Processed batch up to offset {offset}")
        
    all_embeddings = np.vstack(all_embeddings)
    np.save(embeddings_file, all_embeddings)
    np.save(ids_file, np.array(all_ids))
    
    print(f"Saved embeddings to {embeddings_file} and IDs to {ids_file}")
    
    # query = f"""
    # SELECT id, title, directions, ner
    # FROM recipes
    # ORDER BY id
    # """
    
    # dataset = Dataset.from_sql(query, engine)
    
    # texts = [f"{item['title']} {item['directions']} {item['ner']}" for item in dataset]
    # embeddings = model.encode(texts, show_progress_bar=True)
    
    # np.save(embeddings_file, embeddings)
    # np.save(ids_file, np.array([item['id'] for item in dataset]))
    

def load_embeddings(embeddings_file=EMBEDDINGS_FILE, ids_file=IDS_FILE):
    embeddings = np.load(embeddings_file)
    ids = np.load(ids_file)
    return embeddings, ids


def get_top_k_similar(query_title, embeddings, ids, model, k=10):
    query_embedding = model.encode([query_title])
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    top_k_idx = np.argsort(similarities)[-k:][::-1]
    return [(ids[i], similarities[i]) for i in top_k_idx]


if __name__ == "__main__":
    #  - Uncomment to generate and save embeddings
    generate_and_save_embeddings()
    
    # # Load embeddings and model
    # embeddings, ids = load_embeddings()
    # model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
    
    # # Example query
    # query = "chocolate chip cookies"
    # top_results = get_top_k_similar(query, embeddings, ids, model, k=10)
    # print("Top 10 similar recipe IDs and scores:")
    # for rid, score in top_results:
    #     print(f"ID: {rid}, Score: {score}")
