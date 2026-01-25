from model.preprocess import recipe_to_text
from model.embed import embed_texts
from model.similarity import find_similar

# Return top-k recommended recipes similar to a query recipe
def recommend(query_recipe, all_recipes, all_embeddings, top_k=5):
    
    query_text = recipe_to_text(query_recipe)
    query_embedding = embed_texts([query_text])[0]

    top_indices = find_similar(query_embedding, all_embeddings, top_k=top_k)

    recommendations = [all_recipes[i] for i in top_indices]
    return recommendations
