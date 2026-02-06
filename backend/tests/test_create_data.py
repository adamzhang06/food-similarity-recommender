import os
import pandas as pd


def ingest_data(csv_path):
    """This loads in the data from a CSV to make a smaller test CSV

    Args:
        csv_path (str): Takes a file input as a string to my data
    """

    if not os.path.exists(csv_path):
        print(f"File not found: {csv_path}")
        return

    # - Loading into pandas first allows us to handle weird CSV formatting easily
    print(f"Reading CSV from {csv_path}...")
    df = pd.read_csv(csv_path)

    # - Clean column names to be SQL-friendly (lowercase, no spaces)
    df.columns = [c.lower().replace(" ", "_") for c in df.columns]

    # - Insert 'id' column
    if "id" not in df.columns:
        df.insert(0, "id", range(1, 1 + len(df)))

    # - Get 10,000 random samples for testing
    test_df = df.sample(n=10000, random_state=42)

    # - Save to new CSV
    test_csv_path = "backend/data/test_recipes.csv"
    test_df.to_csv(test_csv_path, index=False)
    print(
        f"Success! Created test dataset with 10,000 random recipes at {test_csv_path}."
    )


# --- creating the test dataset ---
if __name__ == "__main__":
    ingest_data("backend/data/recipes_data.csv")
