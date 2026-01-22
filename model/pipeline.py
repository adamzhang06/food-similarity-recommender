from model.load_data import load_recipes
from model.preprocess import clean_ingredients, recipe_to_text
from model.embed import embed_texts

# Full pipeline to load, preprocess, and embed recipes
def run_pipeline(json_path):
    recipes = load_recipes(json_path)

    for r in recipes:
        r["ingredients"] = clean_ingredients(r["ingredients"])

    texts = [recipe_to_text(r) for r in recipes]
    embeddings = embed_texts(texts)

    return recipes, embeddings
