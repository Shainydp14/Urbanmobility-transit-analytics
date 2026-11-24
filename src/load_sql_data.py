import pandas as pd
import sqlite3
import os

# Create database folder
os.makedirs("data", exist_ok=True)

# Connect to SQLite database
connection = sqlite3.connect("data/urbanmobility.db")

datasets = {
    "bus_routes": "data/cleaned/da_bus_routes.csv",
    "ridership": "data/cleaned/da_ridership_data.csv",
    "journey_times": "data/cleaned/da_journey_times.csv"
}

print("\n========== SQL DATABASE SETUP ==========\n")

for table_name, file_path in datasets.items():

    df = pd.read_csv(file_path)

    # Load CSV into SQL table
    df.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False
    )

    print("Table created:", table_name)
    print("Rows:", len(df))

    # Display table columns
    cursor = connection.execute(
        f"PRAGMA table_info({table_name})"
    )

    print("Columns:")

    for column in cursor.fetchall():
        print("-", column[1], column[2])

    print()

print("========== SQL TABLES CREATED ==========")

connection.close()