from scripts.run_pipeline import run_pipeline
from model.recommender import recommend

if __name__ == "__main__":
    # 1. Run the pipeline
    recipes, embeddings = run_pipeline("data/raw/ar.json")

    # 2. Choose a query recipe
    query = recipes[15]
    print("Query recipe:", query["title"])

    # 3. Get recommendations
    top_recipes = recommend(query, recipes, embeddings, top_k=5)

    # 4. Print top recommendations
    print(f"\nTop recommendations for {query}:")
    for i, r in enumerate(top_recipes, 1):
        print(f"{i}. {r['title']}")
