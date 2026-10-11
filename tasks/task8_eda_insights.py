import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# ==================================================
# 1. SETUP
# ==================================================

OUTPUT_DIR = os.path.join("outputs", "task8")
DATA_PATH = os.path.join("data", "retail_sales_clean.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")

print("=" * 60)
print("TASK 8: EXPLORATORY DATA ANALYSIS")
print("=" * 60)

# ==================================================
# 2. LOAD DATASET
# ==================================================

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(
        "Cleaned dataset not found! Please run Task 7 first."
    )

df = pd.read_csv(DATA_PATH)

required_columns = [
    "Order_ID",
    "Order_Date",
    "Category",
    "Region",
    "Units_Sold",
    "Unit_Price_INR",
    "Discount_Pct",
    "Sales_INR",
    "Profit_INR"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:
    raise ValueError(
        f"Required columns are missing: {missing_columns}"
    )

# Convert data types
df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

numeric_columns = [
    "Units_Sold",
    "Unit_Price_INR",
    "Discount_Pct",
    "Sales_INR",
    "Profit_INR"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(
        df[column],
        errors="coerce"
    )

print("\nDataset loaded successfully!")
print(f"Number of rows: {df.shape[0]}")
print(f"Number of columns: {df.shape[1]}")

print("\nFirst 5 Records:")
print(df.head())

print("\nMissing Values:")
print(df.isnull().sum())

# ==================================================
# 3. DESCRIPTIVE STATISTICS
# ==================================================

print("\n" + "=" * 60)
print("DESCRIPTIVE STATISTICS")
print("=" * 60)

descriptive_stats = df[numeric_columns].describe().round(2)

print(descriptive_stats)

descriptive_stats.to_csv(
    os.path.join(OUTPUT_DIR, "descriptive_statistics.csv")
)

# ==================================================
# 4. CATEGORY-WISE SALES ANALYSIS
# ==================================================

print("\n" + "=" * 60)
print("CATEGORY-WISE PERFORMANCE")
print("=" * 60)

category_data = df.dropna(
    subset=["Category", "Sales_INR", "Profit_INR"]
)

category_summary = (
    category_data.groupby("Category")
    .agg(
        Total_Sales=("Sales_INR", "sum"),
        Total_Profit=("Profit_INR", "sum"),
        Total_Units_Sold=("Units_Sold", "sum"),
        Number_of_Orders=("Order_ID", "count")
    )
    .sort_values("Total_Sales", ascending=False)
    .round(2)
)

print(category_summary)

category_summary.to_csv(
    os.path.join(OUTPUT_DIR, "category_summary.csv")
)

# ==================================================
# 5. REGION-WISE SALES ANALYSIS
# ==================================================

print("\n" + "=" * 60)
print("REGION-WISE PERFORMANCE")
print("=" * 60)

region_data = df.dropna(
    subset=["Region", "Sales_INR", "Profit_INR"]
)

region_summary = (
    region_data.groupby("Region")
    .agg(
        Total_Sales=("Sales_INR", "sum"),
        Total_Profit=("Profit_INR", "sum"),
        Total_Units_Sold=("Units_Sold", "sum"),
        Number_of_Orders=("Order_ID", "count")
    )
    .sort_values("Total_Sales", ascending=False)
    .round(2)
)

print(region_summary)

region_summary.to_csv(
    os.path.join(OUTPUT_DIR, "region_summary.csv")
)

# ==================================================
# 6. CORRELATION ANALYSIS
# ==================================================

print("\n" + "=" * 60)
print("CORRELATION MATRIX")
print("=" * 60)

correlation_data = df[numeric_columns]

correlation_matrix = correlation_data.corr().round(2)

print(correlation_matrix)

correlation_matrix.to_csv(
    os.path.join(OUTPUT_DIR, "correlation_matrix.csv")
)

# Correlation Heatmap
plt.figure(figsize=(10, 6))

sns.heatmap(
    correlation_matrix,
    annot=True,
    cmap="coolwarm",
    fmt=".2f",
    linewidths=0.5
)

plt.title("Correlation Heatmap of Retail Sales Data")
plt.tight_layout()

plt.savefig(
    os.path.join(OUTPUT_DIR, "correlation_heatmap.png"),
    dpi=300,
    bbox_inches="tight"
)

plt.close()

print("\nCorrelation heatmap saved successfully.")

# ==================================================
# 7. DAILY SALES TREND
# ==================================================

print("\nGenerating Daily Sales Trend...")

daily_data = df.dropna(
    subset=["Order_Date", "Sales_INR"]
)

daily_sales = (
    daily_data.groupby("Order_Date")["Sales_INR"]
    .sum()
    .sort_index()
)

if not daily_sales.empty:

    plt.figure(figsize=(12, 6))

    plt.plot(
        daily_sales.index,
        daily_sales.values,
        marker="o",
        linewidth=2
    )

    plt.title("Daily Sales Trend")
    plt.xlabel("Order Date")
    plt.ylabel("Total Sales (INR)")
    plt.xticks(rotation=45)
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "daily_sales_trend.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Daily sales trend saved successfully.")

else:
    print("Daily sales trend skipped: no valid date and sales data.")

# ==================================================
# 8. CATEGORY-WISE SALES CHART
# ==================================================

print("Generating Category-wise Sales Chart...")

if not category_summary.empty:

    plt.figure(figsize=(9, 5))

    category_summary["Total_Sales"].plot(
        kind="bar",
        edgecolor="black"
    )

    plt.title("Total Sales by Product Category")
    plt.xlabel("Product Category")
    plt.ylabel("Total Sales (INR)")
    plt.xticks(rotation=20)
    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "category_sales_chart.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Category sales chart saved successfully.")

# ==================================================
# 9. AUTOMATIC BUSINESS INSIGHTS
# ==================================================

print("\n" + "=" * 60)
print("KEY BUSINESS INSIGHTS")
print("=" * 60)

insights = []

if not category_summary.empty:

    best_category = category_summary["Total_Sales"].idxmax()
    best_sales = category_summary.loc[
        best_category, "Total_Sales"
    ]

    insights.append(
        f"The highest-sales category is {best_category}, "
        f"with total sales of INR {best_sales:,.2f}."
    )

    profitable_category = category_summary["Total_Profit"].idxmax()
    highest_profit = category_summary.loc[
        profitable_category, "Total_Profit"
    ]

    insights.append(
        f"The highest-profit category is {profitable_category}, "
        f"with total profit of INR {highest_profit:,.2f}."
    )

if not region_summary.empty:

    best_region = region_summary["Total_Sales"].idxmax()
    best_region_sales = region_summary.loc[
        best_region, "Total_Sales"
    ]

    insights.append(
        f"The highest-sales region is {best_region}, "
        f"with total sales of INR {best_region_sales:,.2f}."
    )

    lowest_region = region_summary["Total_Sales"].idxmin()
    lowest_region_sales = region_summary.loc[
        lowest_region, "Total_Sales"
    ]

    insights.append(
        f"The lowest-sales region is {lowest_region}, "
        f"with total sales of INR {lowest_region_sales:,.2f}."
    )

for number, insight in enumerate(insights, start=1):
    print(f"{number}. {insight}")

# Save insights in a text file
insights_path = os.path.join(
    OUTPUT_DIR,
    "business_insights.txt"
)

with open(insights_path, "w", encoding="utf-8") as file:
    file.write("KEY BUSINESS INSIGHTS\n")
    file.write("=" * 50 + "\n\n")

    for number, insight in enumerate(insights, start=1):
        file.write(f"{number}. {insight}\n")

# ==================================================
# 10. FINAL STATUS
# ==================================================

print("\n" + "=" * 60)
print("TASK 8 COMPLETED SUCCESSFULLY!")
print("=" * 60)

expected_files = [
    "descriptive_statistics.csv",
    "category_summary.csv",
    "region_summary.csv",
    "correlation_matrix.csv",
    "correlation_heatmap.png",
    "daily_sales_trend.png",
    "category_sales_chart.png",
    "business_insights.txt"
]

print("\nOUTPUT FILE STATUS:")

for filename in expected_files:

    file_path = os.path.join(OUTPUT_DIR, filename)

    if os.path.exists(file_path):
        print(f"[OK] {filename}")
    else:
        print(f"[MISSING] {filename}")

print(f"\nAll output files are saved in: {OUTPUT_DIR}")