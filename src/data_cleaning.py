import pandas as pd
import os

files = [
    "da_bus_routes.csv",
    "da_ridership_data.csv",
    "da_journey_times.csv"
]

for file in files:

    path = os.path.join("data", file)

    print("\n" + "=" * 60)
    print("DATASET:", file)
    print("=" * 60)

    df = pd.read_csv(path)

    print("\n1. Dataset Shape:")
    print(df.shape)

    print("\n2. Column Names:")
    print(df.columns.tolist())

    print("\n3. Data Types:")
    print(df.dtypes.to_string())

    print("\n4. Missing Values:")
    print(df.isnull().sum().to_string())

    print("\n5. Duplicate Records:")
    print(df.duplicated().sum())

    print("\n6. First 10 Records:")
    print(df.head(10).to_string(index=False))

    print("\n7. Statistical Summary:")
    print(df.describe(include="all").to_string())

print("\nDATASET INSPECTION COMPLETED!")