import json
from model.load_data import load_recipes
from model.preprocess import clean_ingredients, recipe_to_text
from model.preprocess import clean_master_ingredients

def build_dataset(json_path):
    # Load recipes
    recipes = load_recipes(json_path)  

    for recipe in recipes:
        # Clean ingredients
        recipe["ingredients"] = clean_master_ingredients(recipe["ingredients"])

    return recipes

ar = build_dataset("data/raw/ar.json")
epi = build_dataset("data/raw/epi.json")
fn = build_dataset("data/raw/fn.json")

print(f"Count for ar: {len(ar)} \nCount for epi: {len(epi)} \nCount for fn: {len(fn)}")

