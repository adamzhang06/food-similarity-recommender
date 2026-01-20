from model.load_data import load_recipes

def run_pipeline(json_path):
    recipes = load_recipes(json_path)

    return recipes