import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
from streamlit_autorefresh import st_autorefresh

# PAGE CONFIGURATION
st.set_page_config(
    page_title="UrbanMobility Transit Analytics",
    page_icon="🚌",
    layout="wide"
)

# AUTOMATIC REFRESH
st_autorefresh(interval=30000, key="dashboard_refresh")

# DATASET PATHS
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data" / "cleaned"

# LOAD DATASETS
@st.cache_data(ttl=30)
def load_data():
    ridership = pd.read_csv(DATA_DIR / "da_ridership_data.csv")
    journeys = pd.read_csv(DATA_DIR / "da_journey_times.csv")
    routes = pd.read_csv(DATA_DIR / "da_bus_routes.csv")

    ridership["date"] = pd.to_datetime(
        ridership["date"], errors="coerce"
    )

    journeys["trip_datetime"] = pd.to_datetime(
        journeys["trip_datetime"], errors="coerce"
    )

    return ridership, journeys, routes


try:
    ridership, journeys, routes = load_data()
except Exception as error:
    st.error(f"Unable to load datasets: {error}")
    st.stop()


# DASHBOARD HEADER
st.title("🚌 UrbanMobility Transit Analytics")

st.markdown(
    """
    ### Smart City Transport Performance Dashboard

    Analyze passenger ridership, route performance,
    journey delays and transport efficiency.
    """
)

st.caption("Dashboard refreshes automatically every 30 seconds.")

st.divider()


# SIDEBAR FILTERS
st.sidebar.title("Dashboard Filters")

route_list = sorted(ridership["route_id"].dropna().unique())

selected_routes = st.sidebar.multiselect(
    "Select Routes",
    route_list,
    default=route_list
)

filtered_ridership = ridership[
    ridership["route_id"].isin(selected_routes)
].copy()

filtered_journeys = journeys[
    journeys["route_id"].isin(selected_routes)
].copy()

if filtered_ridership.empty or filtered_journeys.empty:
    st.warning("No data available for the selected routes.")
    st.stop()


# KPI CALCULATIONS
total_passengers = filtered_ridership["daily_passengers"].sum()
average_passengers = filtered_ridership["daily_passengers"].mean()
average_delay = filtered_ridership["avg_delay_min"].mean()
average_on_time = filtered_ridership["on_time_pct"].mean()
total_cancellations = filtered_ridership["cancellations"].sum()
total_routes = filtered_ridership["route_id"].nunique()

scheduled_trips = filtered_ridership["trips_scheduled"].sum()
completed_trips = filtered_ridership["trips_completed"].sum()


# KPI CARDS
st.header("Key Performance Indicators")

col1, col2, col3 = st.columns(3)

col1.metric("Total Passengers", f"{total_passengers:,.0f}")
col2.metric("Average Daily Passengers", f"{average_passengers:,.0f}")
col3.metric("Average Delay", f"{average_delay:.2f} min")

col4, col5, col6 = st.columns(3)

col4.metric("On-Time Performance", f"{average_on_time:.2f}%")
col5.metric("Total Cancellations", f"{total_cancellations:,.0f}")
col6.metric("Routes Selected", total_routes)

st.divider()


# 1. TOP 10 ROUTES BY RIDERSHIP
st.header("1. Top 10 Routes by Passenger Ridership")

top_routes = (
    filtered_ridership.groupby("route_id")["daily_passengers"]
    .sum()
    .nlargest(10)
    .reset_index()
)

fig1 = px.bar(
    top_routes,
    x="route_id",
    y="daily_passengers",
    title="Passenger Ridership by Route",
    labels={
        "route_id": "Route ID",
        "daily_passengers": "Total Passengers"
    },
    text_auto=True
)

st.plotly_chart(fig1, use_container_width=True)


# 2. AVERAGE DELAY BY ROUTE
st.header("2. Average Delay by Route")

route_delay = (
    filtered_ridership.groupby("route_id")["avg_delay_min"]
    .mean()
    .reset_index()
    .sort_values("avg_delay_min", ascending=False)
)

fig2 = px.bar(
    route_delay,
    x="route_id",
    y="avg_delay_min",
    title="Average Delay Across Routes",
    labels={
        "route_id": "Route ID",
        "avg_delay_min": "Average Delay (Minutes)"
    },
    text_auto=".2f"
)

st.plotly_chart(fig2, use_container_width=True)


# 3. PEAK VS OFF-PEAK ANALYSIS
st.header("3. Peak vs Off-Peak Analysis")

peak_data = (
    filtered_journeys.groupby("time_category")
    .agg(
        average_delay=("delay_min", "mean"),
        average_passengers=("passenger_count", "mean")
    )
    .reset_index()
)

fig3 = px.bar(
    peak_data,
    x="time_category",
    y="average_delay",
    title="Average Delay: Peak vs Off-Peak",
    labels={
        "time_category": "Time Category",
        "average_delay": "Average Delay (Minutes)"
    },
    text_auto=".2f"
)

st.plotly_chart(fig3, use_container_width=True)


# 4. HOURLY DELAY ANALYSIS
st.header("4. Hourly Delay Analysis")

hourly_data = (
    filtered_journeys.groupby("hour_of_day")["delay_min"]
    .mean()
    .reset_index()
    .sort_values("hour_of_day")
)

fig4 = px.line(
    hourly_data,
    x="hour_of_day",
    y="delay_min",
    markers=True,
    title="Average Transport Delay by Hour",
    labels={
        "hour_of_day": "Hour of Day",
        "delay_min": "Average Delay (Minutes)"
    }
)

st.plotly_chart(fig4, use_container_width=True)


# 5. WEEKDAY VS WEEKEND RIDERSHIP
st.header("5. Weekday vs Weekend Ridership")

weekend_data = (
    filtered_ridership.groupby("is_weekend")["daily_passengers"]
    .mean()
    .reset_index()
)

weekend_data["Day Type"] = weekend_data["is_weekend"].map({
    "No": "Weekday",
    "Yes": "Weekend"
})

fig5 = px.bar(
    weekend_data,
    x="Day Type",
    y="daily_passengers",
    title="Average Passenger Ridership",
    labels={
        "daily_passengers": "Average Passengers"
    },
    text_auto=".2f"
)

st.plotly_chart(fig5, use_container_width=True)


# 6. SCHEDULED VS COMPLETED TRIPS
st.header("6. Scheduled vs Completed Trips")

trip_data = pd.DataFrame({
    "Trip Type": ["Scheduled", "Completed"],
    "Trips": [scheduled_trips, completed_trips]
})

fig6 = px.bar(
    trip_data,
    x="Trip Type",
    y="Trips",
    title="Scheduled vs Completed Trips",
    text_auto=True
)

st.plotly_chart(fig6, use_container_width=True)


# 7. DELAY PATTERN HEATMAP
st.header("7. Transport Delay Pattern Heatmap")

heatmap_data = filtered_journeys.pivot_table(
    index="hour_of_day",
    columns="time_category",
    values="delay_min",
    aggfunc="mean"
)

fig7 = px.imshow(
    heatmap_data,
    text_auto=".1f",
    aspect="auto",
    color_continuous_scale="YlOrRd",
    labels={
        "x": "Time Category",
        "y": "Hour of Day",
        "color": "Average Delay (Minutes)"
    },
    title="Average Delay by Hour and Time Category"
)

st.plotly_chart(fig7, use_container_width=True)


# 8. ROUTE PERFORMANCE DETAILS
st.header("8. Route Performance Details")

route_summary = (
    filtered_ridership.groupby("route_id")
    .agg(
        total_passengers=("daily_passengers", "sum"),
        average_delay=("avg_delay_min", "mean"),
        average_on_time=("on_time_pct", "mean"),
        cancellations=("cancellations", "sum")
    )
    .reset_index()
)

st.dataframe(
    route_summary,
    use_container_width=True,
    hide_index=True
)


# 9. OPTIMIZATION RECOMMENDATIONS
st.divider()

st.header("9. Data-Driven Optimization Recommendations")

st.write(
    "The following recommendations are based on "
    "the passenger ridership and journey-time analysis."
)

with st.expander("1. Improve High-Delay Routes", expanded=True):
    st.write(
        "Routes R16, R20, R09, R18 and R06 have the "
        "highest average delays. Prioritize these routes "
        "for schedule reviews, operational monitoring "
        "and delay investigation."
    )

with st.expander("2. Optimize Peak-Hour Operations"):
    st.write(
        "Peak periods experience an average delay of "
        "19.84 minutes compared with 3.65 minutes "
        "during off-peak periods. Review vehicle "
        "allocation and departure schedules during busy hours."
    )

with st.expander("3. Increase Capacity on High-Ridership Routes"):
    st.write(
        "Route R03 has the highest passenger ridership, "
        "with 365,091 passengers. Evaluate whether "
        "additional trips or larger-capacity vehicles are required."
    )

with st.expander("4. Improve Weekday Service Planning"):
    st.write(
        "Average weekday ridership is 1,260.98 passengers, "
        "compared with 808.31 on weekends. Consider adjusting "
        "service frequency to match weekday and weekend demand."
    )

with st.expander("5. Reduce Trip Cancellations"):
    st.write(
        "The dataset records 6,733 cancellations. "
        "Investigate cancellation reasons, improve operational "
        "planning and monitor scheduled versus completed trips."
    )

st.info(
    "These recommendations are analytical suggestions. "
    "Their actual impact should be measured after implementation."
)


# FOOTER
st.divider()

st.markdown(
    """
    **UrbanMobility Transit Analytics**

    Data Analytics Capstone Project

    Built using Python, Pandas, Plotly and Streamlit.
    """
)