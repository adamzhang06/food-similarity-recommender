from model.pipeline import run_pipeline

# Run the full pipeline (ONLY IF IT'S BEING RUN DIRECTLY) and print results
if __name__ == "__main__":
    recipes, embeddings = run_pipeline("data/raw/recipes_raw_nosource_ar.json")
    print(f"Processed {len(recipes)} recipes")
    print("Sample recipe:", recipes[0]["title"])
