import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from datasets import Dataset
from backend.ingestion.load_data import get_engine

# ! Getting a sub-dataset from the PostgreSQL database for testing the recommender pipeline
engine = get_engine()

# - Query 10,000 random recipes
query = """
SELECT id, title, directions, ner
FROM recipes
ORDER BY RANDOM()
LIMIT 10000
"""

# - Load into pandas and then convert to Hugging Face Dataset for easier integration with the embedding model
# df = pd.read_sql(query, engine)
# dataset = Dataset.from_pandas(df)

# print(df.head())
# print(dataset[0])

# - Dataset.connect to skip the pandas step
dataset = Dataset.from_sql(query, engine)

# - Example: using 'title' and 'directions' fields
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
texts = [f"{item['title']} {item['directions']} {item['ner']}" for item in dataset]
embeddings = model.encode(texts, show_progress_bar=True)

print(embeddings.shape)  # Should be (10000, embedding_dim)

def get_top_k_similar_sklearn(query_title, embeddings, dataset, k=10):
    query_embedding = model.encode([query_title], convert_to_numpy=True)
    # Compute cosine similarity (returns a (1, num_recipes) array)
    similarities = cosine_similarity(query_embedding, embeddings)[0]
    # Get indices of top k similarities
    top_k_idx = np.argsort(similarities)[-k:][::-1]
    return [dataset[i] for i in top_k_idx]

# Example usage:
query = dataset[0]['title']  # Using the title of the first recipe as a query
top_recipes = get_top_k_similar_sklearn(query, embeddings, dataset, k=10)

print(f"Query: {query}\n")

for recipe in top_recipes:
    print(recipe["title"])
























# def preprocess_text(df):
#     # - Basic preprocessing: lowercase and strip whitespace
    
#     filtered_df = df[
#         df["id"].notnull()
#         & df["title"].notnull()
#         & df["directions"].notnull()
#         & df["ner"].notnull()
#     ]
    
#     recipes_dict = {
#         row["id"]: {
#             "title": row["title"].lower().strip(),
#             "directions": row["directions"].lower().strip(),
#             "ner": row["ner"].lower().strip(),
#         }
#         for _, row in filtered_df.iterrows()
#     }
    
#     return recipes_dict



# # dataset = load_dataset("csv", data_files="backend/data/test_recipes.csv")

# recipes = pd.read_csv("backend/data/test_recipes.csv")


# recipes_dict = preprocess_text(recipes)
# print(list(recipes_dict.items())[:2])