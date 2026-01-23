import json

# Since I have more than one file to load, this function will help load each one
def load_recipes(path):
    with open(path, 'r') as file:
        data = json.load(file)

    recipes = []

    for _, recipe in data.items():

        # There seemed to be some incomplete data entries, so I needed to add this check
        # I only want the recipes that have photos: ~70,000
        if (
            recipe
            and recipe.get("title")
            and recipe.get("ingredients")
            and recipe.get("instructions")
            and recipe.get("picture_link")
        ):
            recipes.append({
                'title': recipe['title'],
                'ingredients': recipe['ingredients'],
                'instructions': recipe['instructions'],
                'picture_link': recipe['picture_link']
            })

    return recipes

# CODE FOR TESTING: ADDED KEYBOARD SHORTCUT FOR SHIFT + ENTER TO SAVE AND RUN FILE

# recipes = load_recipes("data/raw/recipes_raw_nosource_ar.json")

# print(f"Loaded {len(recipes)} recipes")
# print("\nFirst recipe:")
# print(recipes[0])