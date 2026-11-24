import pandas as pd
import matplotlib.pyplot as plt
import os

# Create output folder
os.makedirs("reports/eda", exist_ok=True)

# Dataset paths
files = {
    "Bus Routes": "data/cleaned/da_bus_routes.csv",
    "Ridership": "data/cleaned/da_ridership_data.csv",
    "Journey Times": "data/cleaned/da_journey_times.csv"
}

print("\n========== URBAN MOBILITY EDA ==========\n")

for name, path in files.items():

    print("\n----------------------------------")
    print("ANALYZING:", name)
    print("----------------------------------")

    df = pd.read_csv(path)

    # Dataset information
    print("\nDataset Shape:", df.shape)

    print("\nColumn Names:")
    print(df.columns.tolist())

    # Numerical analysis
    numeric_columns = df.select_dtypes(
        include="number"
    ).columns.tolist()

    if numeric_columns:

        print("\nNumerical Summary:")
        print(df[numeric_columns].describe().to_string())

        # Create histograms
        for column in numeric_columns:

            plt.figure(figsize=(9, 5))

            df[column].dropna().hist(bins=20)

            plt.title(f"{name} - {column} Distribution")
            plt.xlabel(column)
            plt.ylabel("Frequency")

            plt.tight_layout()

            filename = (
                f"reports/eda/{name.replace(' ', '_')}"
                f"_{column}_distribution.png"
            )

            plt.savefig(filename)
            plt.close()

            print("Chart saved:", filename)

    # Categorical analysis
    categorical_columns = df.select_dtypes(
        include=["object", "string"]
    ).columns.tolist()

    for column in categorical_columns:

        if df[column].nunique() <= 20:

            plt.figure(figsize=(10, 5))

            df[column].value_counts().head(10).plot(
                kind="bar"
            )

            plt.title(f"{name} - {column} Distribution")
            plt.xlabel(column)
            plt.ylabel("Count")

            plt.xticks(rotation=45)
            plt.tight_layout()

            filename = (
                f"reports/eda/{name.replace(' ', '_')}"
                f"_{column}_distribution.png"
            )

            plt.savefig(filename)
            plt.close()

            print("Chart saved:", filename)

print("\n========== EDA COMPLETED SUCCESSFULLY ==========")