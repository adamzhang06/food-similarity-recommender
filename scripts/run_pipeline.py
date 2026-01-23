import json
from model.load_data import load_recipes
from model.preprocess import clean_ingredients, recipe_to_text
from model.embed import embed_texts

# Full pipeline to load, preprocess, and embed recipes
def run_pipeline(json_path):
    # Load recipes
    recipes = load_recipes(json_path)  

    for recipe in recipes:
        # Clean ingredients
        recipe["ingredients"] = clean_ingredients(recipe["ingredients"])

    # Convert recipes to text
    recipe_texts = [recipe_to_text(r) for r in recipes]

    # Generate embeddings
    embeddings = embed_texts(recipe_texts)

    return recipes, embeddings
