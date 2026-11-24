import sqlite3
import pandas as pd

# Connect to database
connection = sqlite3.connect("data/urbanmobility.db")

print("\n========== URBAN MOBILITY SQL ANALYSIS ==========\n")

# Display available tables
tables = pd.read_sql_query(
    "SELECT name FROM sqlite_master WHERE type='table'",
    connection
)

print("AVAILABLE TABLES:")
print(tables.to_string(index=False))

# SQL Queries
queries = {
    "Total Bus Routes":
        "SELECT COUNT(*) AS total_routes FROM bus_routes",

    "Total Ridership Records":
        "SELECT COUNT(*) AS total_records FROM ridership",

    "Total Journey Records":
        "SELECT COUNT(*) AS total_journeys FROM journey_times",

    "Bus Routes Sample":
        "SELECT * FROM bus_routes LIMIT 5",

    "Ridership Sample":
        "SELECT * FROM ridership LIMIT 5",

    "Journey Times Sample":
        "SELECT * FROM journey_times LIMIT 5"
}

# Execute queries
for title, query in queries.items():

    print("\n----------------------------------------")
    print(title)
    print("----------------------------------------")

    result = pd.read_sql_query(query, connection)

    print(result.to_string(index=False))

connection.close()

print("\n========== SQL ANALYSIS COMPLETED ==========")