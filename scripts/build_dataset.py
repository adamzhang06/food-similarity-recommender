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

# ar = build_dataset("data/raw/ar.json")
# epi = build_dataset("data/raw/epi.json")
# fn = build_dataset("data/raw/fn.json")

# print(f"Count for ar: {len(ar)} \nCount for epi: {len(epi)} \nCount for fn: {len(fn)}")

# Comine all recipe JSON files into one dataset. Takes in a list of JSON file paths and removes duplicates based on recipe title.
def combine_datasets(json_paths, dedupe=True):
    combined = []
    seen_titles = set()

    for path in json_paths:
        recipes = build_dataset(path)

        for recipe in recipes:
            title = recipe.get("title")

            if dedupe:
                if not title or title in seen_titles:
                    continue
                seen_titles.add(title)

            combined.append(recipe)

    return combined

json_files = [
    "data/raw/ar.json",
    "data/raw/epi.json",
    "data/raw/fn.json",
]

master_recipes = combine_datasets(json_files)

output_path = "data/processed/master_recipes.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(master_recipes, f, ensure_ascii=False, indent=2)

# print(f"Total recipes: {len(master_recipes)}")
# print(master_recipes[100])