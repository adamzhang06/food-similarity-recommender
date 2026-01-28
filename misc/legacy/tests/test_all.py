from model.load_data import load_recipes
from model.preprocess import clean_ingredients, recipe_to_text
from model.embed import embed_texts

recipes_ar = load_recipes("data/raw/recipes_raw_nosource_ar.json")
# recipes_epi = load_recipes("data/raw/recipes_raw_nosource_epi.json")
# recipes_fn = load_recipes("data/raw/recipes_raw_nosource_fn.json")

# print("\n",recipes_ar[0], "\n")

recipes_ar_copy = recipes_ar.copy()

for r in recipes_ar_copy:
    r['ingredients'] = clean_ingredients(r['ingredients'])

# print(len(recipes_ar_copy))

# recipes_ar_texts = [recipe_to_text(r) for r in recipes_ar_copy]

# print(recipes_ar_texts[0])

# recipes_ar_embeddings = embed_texts(recipes_ar_texts)

