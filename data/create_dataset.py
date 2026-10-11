import os
import numpy as np
import pandas as pd

np.random.seed(42)

# Number of records
n = 120

# Generate dates
dates = pd.date_range(
    start="2025-01-01",
    periods=n,
    freq="D"
)

# Product categories
categories = np.random.choice(
    ["Electronics", "Home & Kitchen", "Clothing", "Books"],
    n
)

# Regions
regions = np.random.choice(
    ["North", "South", "East", "West"],
    n
)

# Units sold
units_sold = np.random.randint(1, 12, n)

# Product prices
price_map = {
    "Electronics": 2200,
    "Home & Kitchen": 850,
    "Clothing": 650,
    "Books": 320
}

unit_prices = np.array([
    price_map[category] for category in categories
])

# Add price variation
unit_prices = np.round(
    unit_prices * np.random.uniform(0.75, 1.30, n),
    2
)

# Discounts
discounts = np.random.choice(
    [0, 5, 10, 15, 20],
    n
)

# Sales calculation
sales = np.round(
    units_sold * unit_prices * (1 - discounts / 100),
    2
)

# Profit calculation
cost_rate = np.random.uniform(0.58, 0.82, n)

profit = np.round(
    sales * (1 - cost_rate),
    2
)

# Create DataFrame
df = pd.DataFrame({
    "Order_ID": [
        f"ORD{i:04d}" for i in range(1, n + 1)
    ],
    "Order_Date": dates,
    "Category": categories,
    "Region": regions,
    "Units_Sold": units_sold,
    "Unit_Price_INR": unit_prices,
    "Discount_Pct": discounts,
    "Sales_INR": sales,
    "Profit_INR": profit,
    "Customer_ID": np.random.randint(1001, 1061, n)
})

# Introduce data-quality issues for Task 7

df.loc[7, "Region"] = None
df.loc[18, "Category"] = None
df.loc[29, "Units_Sold"] = np.nan

df.loc[40, "Category"] = "electronics"
df.loc[55, "Region"] = "north "

df.loc[70, "Sales_INR"] = -250
df.loc[85, "Discount_Pct"] = 150

# Add a duplicate record
df = pd.concat(
    [df, df.iloc[[10]]],
    ignore_index=True
)

# Save raw dataset
output_path = os.path.join(
    os.path.dirname(__file__),
    "retail_sales_raw.csv"
)

df.to_csv(output_path, index=False)

print("Dataset created successfully!")
print("Dataset shape:", df.shape)
print("\nFirst five records:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate records:", df.duplicated().sum())