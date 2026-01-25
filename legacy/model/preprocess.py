import re

# Remove unwanted characters and normalize ingredients
def clean_ingredients(ingredients):
    cleaned = []
    for ing in ingredients:
        ing = ing.replace("ADVERTISEMENT", "")
        ing = ing.lower()
        ing = re.sub(r"[^a-z\s]", "", ing)
        cleaned.append(ing.strip())
    return cleaned

# Convert recipe dict into one text string for embedding
def recipe_to_text(recipe):
    ingredients = " ".join(recipe["ingredients"])
    return f"{recipe['title']}. Ingredients: {ingredients}. Instructions: {recipe['instructions']}"

# Setup master database for all recipes
def clean_master_ingredients(ingredients):
    cleaned = []
    for ing in ingredients:
        ing = ing.replace("ADVERTISEMENT", "")
        cleaned.append(ing.strip())
    return cleaned