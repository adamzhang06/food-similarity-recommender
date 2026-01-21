from model.load_data import load_recipes
from model.preprocess import clean_ingredients, recipe_to_text

recipes_ar = load_recipes("data/raw/recipes_raw_nosource_ar.json")

# print("\n",recipes_ar[0], "\n")

recipes_ar_copy = recipes_ar.copy()

for r in recipes_ar_copy:
    r['ingredients'] = clean_ingredients(r['ingredients'])

print("\n\n OUTPUT BELOW \n\n",recipes_ar_copy[0]['ingredients'], "\n\n OUTPUT ABOVE \n\n")