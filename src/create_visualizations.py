import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "cleaned"
OUTPUT_DIR = BASE_DIR / "reports" / "visualizations"

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Load datasets
ridership = pd.read_csv(DATA_DIR / "da_ridership_data.csv")
journeys = pd.read_csv(DATA_DIR / "da_journey_times.csv")

# Convert numeric columns
ridership["daily_passengers"] = pd.to_numeric(
    ridership["daily_passengers"], errors="coerce"
)

ridership["avg_delay_min"] = pd.to_numeric(
    ridership["avg_delay_min"], errors="coerce"
)

journeys["delay_min"] = pd.to_numeric(
    journeys["delay_min"], errors="coerce"
)

journeys["hour_of_day"] = pd.to_numeric(
    journeys["hour_of_day"], errors="coerce"
)

sns.set_theme(style="whitegrid")


# --------------------------------------------------
# 1. TOP 10 ROUTES BY RIDERSHIP
# --------------------------------------------------

top_routes = (
    ridership.groupby("route_id")["daily_passengers"]
    .sum()
    .nlargest(10)
    .sort_values()
)

plt.figure(figsize=(10, 6))
top_routes.plot(kind="barh")

plt.title("Top 10 Routes by Total Passenger Ridership")
plt.xlabel("Total Passengers")
plt.ylabel("Route ID")
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "top_10_routes_ridership.png", dpi=300)
plt.close()


# --------------------------------------------------
# 2. AVERAGE DELAY BY ROUTE
# --------------------------------------------------

route_delays = (
    ridership.groupby("route_id")["avg_delay_min"]
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12, 6))
route_delays.plot(kind="bar")

plt.title("Average Delay by Route")
plt.xlabel("Route ID")
plt.ylabel("Average Delay (Minutes)")
plt.xticks(rotation=45)
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "average_delay_by_route.png", dpi=300)
plt.close()


# --------------------------------------------------
# 3. PEAK VS OFF-PEAK DELAY
# --------------------------------------------------

peak_analysis = (
    journeys.groupby("time_category")["delay_min"]
    .mean()
)

plt.figure(figsize=(8, 5))
peak_analysis.plot(kind="bar")

plt.title("Average Delay: Peak vs Off-Peak")
plt.xlabel("Time Category")
plt.ylabel("Average Delay (Minutes)")
plt.xticks(rotation=0)
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "peak_vs_offpeak_delay.png", dpi=300)
plt.close()


# --------------------------------------------------
# 4. HOURLY DELAY ANALYSIS
# --------------------------------------------------

hourly_delay = (
    journeys.groupby("hour_of_day")["delay_min"]
    .mean()
    .sort_index()
)

plt.figure(figsize=(10, 5))
hourly_delay.plot(kind="line", marker="o")

plt.title("Average Transport Delay by Hour")
plt.xlabel("Hour of Day")
plt.ylabel("Average Delay (Minutes)")
plt.xticks(range(6, 22))
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "hourly_delay_analysis.png", dpi=300)
plt.close()


# --------------------------------------------------
# 5. WEEKDAY VS WEEKEND RIDERSHIP
# --------------------------------------------------

weekend_analysis = (
    ridership.groupby("is_weekend")["daily_passengers"]
    .mean()
    .reindex(["No", "Yes"])
)

plt.figure(figsize=(8, 5))
weekend_analysis.plot(kind="bar")

plt.title("Average Passenger Ridership: Weekday vs Weekend")
plt.xlabel("Day Type")
plt.ylabel("Average Daily Passengers")
plt.xticks([0, 1], ["Weekday", "Weekend"], rotation=0)
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "weekday_vs_weekend.png", dpi=300)
plt.close()


# --------------------------------------------------
# 6. SCHEDULED VS COMPLETED TRIPS
# --------------------------------------------------

trip_data = pd.DataFrame({
    "Trip Type": ["Scheduled", "Completed"],
    "Number of Trips": [
        ridership["trips_scheduled"].sum(),
        ridership["trips_completed"].sum()
    ]
})

plt.figure(figsize=(8, 5))
plt.bar(
    trip_data["Trip Type"],
    trip_data["Number of Trips"]
)

plt.title("Scheduled Trips vs Completed Trips")
plt.xlabel("Trip Type")
plt.ylabel("Number of Trips")
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "scheduled_vs_completed_trips.png", dpi=300)
plt.close()


# --------------------------------------------------
# 7. DELAY PATTERN HEATMAP
# --------------------------------------------------

heatmap_data = journeys.pivot_table(
    index="hour_of_day",
    columns="time_category",
    values="delay_min",
    aggfunc="mean"
)

plt.figure(figsize=(8, 7))

sns.heatmap(
    heatmap_data,
    annot=True,
    fmt=".1f",
    cmap="YlOrRd",
    linewidths=0.5
)

plt.title("Transport Delay Pattern Heatmap")
plt.xlabel("Time Category")
plt.ylabel("Hour of Day")
plt.tight_layout()

plt.savefig(OUTPUT_DIR / "delay_pattern_heatmap.png", dpi=300)
plt.close()


print("\n========================================")
print("ALL VISUALIZATIONS CREATED SUCCESSFULLY!")
print("========================================")

print(f"\nCharts saved in: {OUTPUT_DIR}")

for file in OUTPUT_DIR.glob("*.png"):
    print(file.name)