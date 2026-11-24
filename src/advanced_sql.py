import sqlite3
import pandas as pd

# Connect to database
connection = sqlite3.connect("data/urbanmobility.db")

print("\n========== ADVANCED SQL ANALYSIS ==========\n")

queries = {

    "1. Total Number of Routes":
    """
    SELECT COUNT(*) AS total_routes
    FROM bus_routes;
    """,

    "2. Total Passenger Ridership":
    """
    SELECT SUM(daily_passengers) AS total_passengers
    FROM ridership;
    """,

    "3. Average Daily Passengers":
    """
    SELECT ROUND(AVG(daily_passengers), 2) AS average_passengers
    FROM ridership;
    """,

    "4. Top 10 Routes by Ridership":
    """
    SELECT route_id,
           SUM(daily_passengers) AS total_passengers
    FROM ridership
    GROUP BY route_id
    ORDER BY total_passengers DESC
    LIMIT 10;
    """,

    "5. Routes with Highest Average Delay":
    """
    SELECT route_id,
           ROUND(AVG(avg_delay_min), 2) AS average_delay
    FROM ridership
    GROUP BY route_id
    ORDER BY average_delay DESC;
    """,

    "6. Average On-Time Performance":
    """
    SELECT ROUND(AVG(on_time_pct), 2) AS average_on_time
    FROM ridership;
    """,

    "7. Total Trip Cancellations":
    """
    SELECT SUM(cancellations) AS total_cancellations
    FROM ridership;
    """,

    "8. Scheduled vs Completed Trips":
    """
    SELECT
        SUM(trips_scheduled) AS scheduled_trips,
        SUM(trips_completed) AS completed_trips
    FROM ridership;
    """,

    "9. Peak vs Off-Peak Journey Analysis":
    """
    SELECT
        time_category,
        COUNT(*) AS total_journeys,
        ROUND(AVG(delay_min), 2) AS average_delay,
        ROUND(AVG(passenger_count), 2) AS average_passengers
    FROM journey_times
    GROUP BY time_category;
    """,

    "10. Hourly Delay Analysis":
    """
    SELECT
        hour_of_day,
        ROUND(AVG(delay_min), 2) AS average_delay,
        COUNT(*) AS total_journeys
    FROM journey_times
    GROUP BY hour_of_day
    ORDER BY average_delay DESC;
    """,

    "11. Highest Journey Delays":
    """
    SELECT
        route_id,
        ROUND(AVG(delay_min), 2) AS average_delay,
        MAX(delay_min) AS maximum_delay
    FROM journey_times
    GROUP BY route_id
    ORDER BY average_delay DESC;
    """,

    "12. Weekend vs Weekday Ridership":
    """
    SELECT
        is_weekend,
        ROUND(AVG(daily_passengers), 2) AS average_passengers
    FROM ridership
    GROUP BY is_weekend;
    """
}

# Execute all queries
for title, query in queries.items():

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    result = pd.read_sql_query(query, connection)

    print(result.to_string(index=False))

connection.close()

print("\n========== ADVANCED SQL ANALYSIS COMPLETED ==========")