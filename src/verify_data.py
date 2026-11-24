import sqlite3
import pandas as pd
from pathlib import Path

# Get the project folder
BASE_DIR = Path(__file__).resolve().parent.parent

# Get the database path
DB_PATH = BASE_DIR / "data" / "urbanmobility.db"

print("Database location:", DB_PATH)

# Check database existence
if not DB_PATH.exists():
    print("ERROR: Database file not found!")
    exit()

# Connect to database
conn = sqlite3.connect(str(DB_PATH))

print("\n--- DATASET COUNTS ---")

for table in ["bus_routes", "ridership", "journey_times"]:
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    print(f"{table}: {len(df)} records")

print("\n--- ROUTE ID VERIFICATION ---")

routes = pd.read_sql_query(
    "SELECT DISTINCT route_id FROM bus_routes", conn
)

ridership = pd.read_sql_query(
    "SELECT DISTINCT route_id FROM ridership", conn
)

journeys = pd.read_sql_query(
    "SELECT DISTINCT route_id FROM journey_times", conn
)

master_ids = set(routes["route_id"].dropna())
ridership_ids = set(ridership["route_id"].dropna())
journey_ids = set(journeys["route_id"].dropna())

print("Bus routes:", sorted(master_ids))
print("Ridership routes:", sorted(ridership_ids))
print("Journey routes:", sorted(journey_ids))

print("\n--- UNMATCHED ROUTES ---")
print("Unmatched in ridership:", sorted(ridership_ids - master_ids))
print("Unmatched in journeys:", sorted(journey_ids - master_ids))

conn.close()

print("\nDATA VERIFICATION COMPLETED!")