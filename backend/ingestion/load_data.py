import psycopg2
import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from tqdm import tqdm

# ! Example psycopg2 connection (not used in final code)
# conn = psycopg2.connect(
#     dbname="fooddb",
#     user="fooduser",
#     password="foodpass",
#     host="localhost",
#     port=5432
# )

# ! Load env vars for local dev (Docker will override these automatically)
load_dotenv()


def get_engine():
    """Creates a SQLAlchemy engine for connecting to the PostgreSQL database.

    Returns:
        engine: SQLAlchemy engine instance for the PostgreSQL database connection.

        By using 'db' as the default host, it's ready for Docker Compose service names,
        but falls back to 'localhost' if that env var isn't set.
    """

    user = os.getenv("POSTGRES_USER", "postgres")
    password = os.getenv("POSTGRES_PASSWORD", "password")
    # ! In Docker, this will be the service name (e.g., 'db'). Locally, it's 'localhost'.
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db_name = os.getenv("POSTGRES_DB", "food_recommender")
    
    return create_engine(f"postgresql://{user}:{password}@{host}:{port}/{db_name}")


def ingest_data(csv_path):
    """This loads in the data from a CSV into the PostgreSQL database.

    Args:
        csv_path (str): Takes a file input as a string to my data
    """

    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return

    print("Connecting to database...")
    engine = get_engine()
    
    # - Loading into pandas first allows us to handle weird CSV formatting easily
    print(f"Reading CSV from {csv_path}...")
    df = pd.read_csv(csv_path)
    
    # - Clean column names to be SQL-friendly (lowercase, no spaces)
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]
    
    # - Insert 'id' column
    if "id" not in df.columns:
        df.insert(0, "id", range(1, 1 + len(df)))
    
    # - 'chunksize' helps since my CSV is 2 million+ (prevents memory crash)
    print("Uploading to PostgreSQL with progress bar...")
    chunksize = 1000
    n_chunks = (len(df) + chunksize - 1) // chunksize
    
    for i in tqdm(
        range(0, len(df), chunksize), desc="Uploading", unit="chunk", total=n_chunks
    ):
        chunk = df.iloc[i : i + chunksize]
        chunk.to_sql(
            "recipes", engine, if_exists="replace" if i == 0 else "append", index=False
        )
    
    # - Done loading
    print(f"Success! Uploaded {len(df)} recipes to table 'recipes'.")


def get_recipe_details(recipe_id):
    """Gets recipe details by ID from the database.
    
    Args:
        recipe_id (int): The ID of the recipe to retrieve.
    
    Returns:
        dict or None: A dictionary with recipe details if found, otherwise None.
    """
    
    engine = get_engine()
    
    # - Parameterized query ( :id ) to prevent SQL Injection
    query = text(
        """
        SELECT title, ingredients, directions, link, source, NER, site 
        FROM recipes 
        WHERE id = :id
    """
    )

    with engine.connect() as conn:
        result = conn.execute(query, {"id": recipe_id}).fetchone()

        if result:
            # - Convert SQLAlchemy row to a standard dictionary
            return dict(result._mapping)
        else:
            return None


# # --- usage example ---
# if __name__ == "__main__":
#     # * 1. Run Ingestion (Only need to do this when data changes)
#     # ingest_data("backend/data/recipes_data.csv")
    
#     # * 2. Simulate User Selection
#     # ^ Recipe ID #42 as an example
#     selected_id = 42
#     recipes = get_recipe_details(selected_id)
    
#     if recipes:
#         print(f"--- Recipe Found: {recipes['title']} ---")
#         print(f"Ingredients: {recipes['ingredients'][:50]}...")  # preview
#         print(f"Directions: {recipes['directions'][:50]}...")  # preview
#         print(f"NER: {recipes['ner'][:50]}...")  # preview
#     else:
#         print("Recipe not found.")
