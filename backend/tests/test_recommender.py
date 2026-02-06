from sentence_transformers import SentenceTransformer
from datasets import load_dataset
import pandas as pd


model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# dataset = load_dataset("csv", data_files="backend/data/test_recipes.csv")

recipes = pd.read_csv("backend/data/test_recipes.csv")

# print(dataset.column_names)


def preprocess_text(df):
    # - Basic preprocessing: lowercase and strip whitespace

    filtered_df = df[
        df['id'].notnull()
        & df["title"].notnull()
        & df["directions"].notnull()
        & df["ner"].notnull()
    ]
    
    recipes_dict = {
        row["id"]: {
            "title": row["title"].lower().strip(),
            "directions": row["directions"].lower().strip(),
            "ner": row["ner"].lower().strip()
        }
        
        for _, row in filtered_df.iterrows()
    }
    
    
    return recipes_dict


# dataset = preprocess_text(dataset)

# print(dataset.select_columns(["ingredients", "source", "site"]))

recipes_dict = preprocess_text(recipes)
print(list(recipes_dict.items())[:2])