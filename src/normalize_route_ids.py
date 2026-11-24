import pandas as pd
import re
import sqlite3
from pathlib import Path

# Project folders
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
CLEANED_DIR = DATA_DIR / "cleaned"

# Dataset filenames
files = {
    "bus_routes": CLEANED_DIR / "da_bus_routes.csv",
    "ridership": CLEANED_DIR / "da_ridership_data.csv",
    "journey_times": CLEANED_DIR / "da_journey_times.csv"
}

def normalize_route_id(value):
    if pd.isna(value):
        return value

    match = re.fullmatch(r"R0*(\d+)", str(value).strip(), re.IGNORECASE)

    if match:
        return "R" + match.group(1).zfill(2)

    return str(value).strip()


# Read and normalize datasets
datasets = {}

for table_name, file_path in files.items():

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    df = pd.read_csv(file_path)

    if "route_id" not in df.columns:
        raise ValueError(f"route_id column missing in {file_path.name}")

    df["route_id"] = df["route_id"].apply(normalize_route_id)

    df.to_csv(file_path, index=False)

    datasets[table_name] = df

    print(f"\n{table_name.upper()}")
    print("Total records:", len(df))
    print("Unique routes:", df["route_id"].nunique())
    print("Route IDs:", sorted(df["route_id"].dropna().unique()))


# Check whether all route IDs exist in the master route table
master_routes = set(datasets["bus_routes"]["route_id"].dropna().unique())

for table_name in ["ridership", "journey_times"]:

    dataset_routes = set(
        datasets[table_name]["route_id"].dropna().unique()
    )

    unmatched = dataset_routes - master_routes

    print(f"\nUnmatched routes in {table_name}:")

    if unmatched:
        print(sorted(unmatched))
    else:
        print("None")


# Reload normalized datasets into SQLite
db_path = DATA_DIR / "urbanmobility.db"

with sqlite3.connect(db_path) as connection:

    for table_name, df in datasets.items():
        df.to_sql(
            table_name,
            connection,
            if_exists="replace",
            index=False
        )

print("\nRoute ID normalization completed!")
print("SQLite database updated successfully.")