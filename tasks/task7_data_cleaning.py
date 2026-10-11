import os
import pandas as pd
import numpy as np

# File paths
input_path = "data/retail_sales_raw.csv"
output_path = "data/retail_sales_clean.csv"

# Check whether the dataset exists
if not os.path.exists(input_path):
    raise FileNotFoundError(
        "Raw dataset not found. Run data/create_dataset.py first."
    )

# Load raw dataset
df = pd.read_csv(input_path)

# Create output folder
os.makedirs("outputs/task7", exist_ok=True)

# Display original dataset information
print("=" * 55)
print("TASK 7: EXPLORATORY DATA ANALYSIS AND DATA CLEANING")
print("=" * 55)

print("\n1. ORIGINAL DATASET SHAPE")
print(df.shape)

print("\n2. COLUMN NAMES")
print(df.columns.tolist())

print("\n3. DATA TYPES")
print(df.dtypes)

print("\n4. STATISTICAL SUMMARY")
print(df.describe(include="all").to_string())

print("\n5. MISSING VALUES BEFORE CLEANING")
print(df.isnull().sum())

print("\n6. DUPLICATES BEFORE CLEANING")
print(df.duplicated().sum())

# Save original dataset preview
df.head(20).to_csv(
    "outputs/task7/before_cleaning.csv",
    index=False
)

# Standardize text columns
df["Category"] = df["Category"].astype("string").str.strip().str.title()
df["Region"] = df["Region"].astype("string").str.strip().str.title()

# Standardize known category variations
df["Category"] = df["Category"].replace({
    "Electronics": "Electronics",
    "Home & Kitchen": "Home & Kitchen",
    "Clothing": "Clothing",
    "Books": "Books"
})

# Convert date column
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

# Convert numeric columns
numeric_columns = [
    "Units_Sold",
    "Unit_Price_INR",
    "Discount_Pct",
    "Sales_INR",
    "Profit_INR",
    "Customer_ID"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Remove rows without essential identifiers or dates
df = df.dropna(subset=["Order_ID", "Order_Date"])

# Handle missing categories and regions
for column in ["Category", "Region"]:
    valid_values = df[column].dropna()

    if not valid_values.empty:
        df[column] = df[column].fillna(valid_values.mode().iloc[0])

# Remove rows with invalid category or region values
valid_categories = [
    "Electronics",
    "Home & Kitchen",
    "Clothing",
    "Books"
]

valid_regions = [
    "North",
    "South",
    "East",
    "West"
]

df = df[df["Category"].isin(valid_categories)]
df = df[df["Region"].isin(valid_regions)]

# Remove exact duplicate records
df = df.drop_duplicates()

# Remove duplicate order IDs, keeping the first occurrence
df = df.drop_duplicates(subset=["Order_ID"], keep="first")

# Fix invalid units sold
df.loc[df["Units_Sold"] <= 0, "Units_Sold"] = np.nan

valid_units = df.loc[df["Units_Sold"] > 0, "Units_Sold"]

if not valid_units.empty:
    df["Units_Sold"] = df["Units_Sold"].fillna(valid_units.median())

# Fix invalid unit prices
df.loc[df["Unit_Price_INR"] <= 0, "Unit_Price_INR"] = np.nan

valid_prices = df.loc[df["Unit_Price_INR"] > 0, "Unit_Price_INR"]

if not valid_prices.empty:
    df["Unit_Price_INR"] = df["Unit_Price_INR"].fillna(
        valid_prices.median()
    )

# Fix invalid discounts
df.loc[
    (df["Discount_Pct"] < 0) | (df["Discount_Pct"] > 100),
    "Discount_Pct"
] = np.nan

valid_discounts = df.loc[
    df["Discount_Pct"].between(0, 100),
    "Discount_Pct"
]

if not valid_discounts.empty:
    df["Discount_Pct"] = df["Discount_Pct"].fillna(
        valid_discounts.median()
    )

# Fill missing numeric values
for column in ["Units_Sold", "Unit_Price_INR", "Discount_Pct"]:
    if df[column].isna().any():
        df[column] = df[column].fillna(df[column].median())

# Recalculate sales to correct invalid or missing sales values
expected_sales = (
    df["Units_Sold"]
    * df["Unit_Price_INR"]
    * (1 - df["Discount_Pct"] / 100)
).round(2)

invalid_sales = (
    df["Sales_INR"].isna()
    | (df["Sales_INR"] < 0)
)

df.loc[invalid_sales, "Sales_INR"] = expected_sales[invalid_sales]

# Replace missing or negative profit with an estimated profit
invalid_profit = df["Profit_INR"].isna() | (df["Profit_INR"] < 0)

estimated_profit = (df["Sales_INR"] * 0.20).round(2)

df.loc[invalid_profit, "Profit_INR"] = estimated_profit[invalid_profit]

# Fill any remaining numeric missing values
for column in numeric_columns:
    if df[column].isna().any():
        median_value = df[column].median()

        if pd.notna(median_value):
            df[column] = df[column].fillna(median_value)

# Save cleaned dataset
df.to_csv(output_path, index=False)

# Save cleaned preview
df.head(20).to_csv(
    "outputs/task7/after_cleaning.csv",
    index=False
)

# Display final results
print("\n" + "=" * 55)
print("CLEANING COMPLETED")
print("=" * 55)

print("\nCLEANED DATASET SHAPE")
print(df.shape)

print("\nMISSING VALUES AFTER CLEANING")
print(df.isnull().sum())

print("\nDUPLICATE RECORDS AFTER CLEANING")
print(df.duplicated().sum())

print("\nCLEANED DATASET PREVIEW")
print(df.head(10).to_string(index=False))

print(f"\nCleaned dataset saved at: {output_path}")
print("Before-cleaning preview saved in outputs/task7/")
print("After-cleaning preview saved in outputs/task7/")