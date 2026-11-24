import pandas as pd
import os

os.makedirs("data/cleaned", exist_ok=True)

files = [
    "da_bus_routes.csv",
    "da_ridership_data.csv",
    "da_journey_times.csv"
]

for file in files:

    path = os.path.join("data", file)

    df = pd.read_csv(path)

    print("\nCleaning:", file)

    # Remove duplicate records
    before = len(df)
    df = df.drop_duplicates()

    print("Duplicates removed:", before - len(df))

    # Handle missing values
    for column in df.columns:

        if pd.api.types.is_numeric_dtype(df[column]):

            median_value = df[column].median()

            if pd.notna(median_value):
                df[column] = df[column].fillna(median_value)

        else:
            df[column] = df[column].fillna("Unknown")

    # Save cleaned dataset
    output_file = os.path.join("data/cleaned", file)

    df.to_csv(output_file, index=False)

    print("Cleaned file saved:", output_file)

    print("Remaining missing values:", df.isnull().sum().sum())

print("\nALL DATASETS CLEANED SUCCESSFULLY!")