import os
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv("data/retail_sales_clean.csv")

df["Order_Date"] = pd.to_datetime(
    df["Order_Date"],
    errors="coerce"
)

# Create output folder
os.makedirs("outputs/task5", exist_ok=True)

print("TASK 5: MATPLOTLIB VISUALIZATIONS")
print("-" * 40)

# 1. LINE CHART
daily_sales = (
    df.groupby("Order_Date")["Sales_INR"]
    .sum()
    .sort_index()
)

plt.figure(figsize=(10, 5))
plt.plot(daily_sales.index, daily_sales.values, marker="o")
plt.title("Daily Sales Trend")
plt.xlabel("Order Date")
plt.ylabel("Sales (INR)")
plt.xticks(rotation=45)
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("outputs/task5/line_chart.png", dpi=300)
plt.close()

print("1. Line chart saved successfully!")

# 2. BAR CHART
category_sales = df.groupby("Category")["Sales_INR"].sum()

plt.figure(figsize=(8, 5))
plt.bar(category_sales.index, category_sales.values)
plt.title("Total Sales by Category")
plt.xlabel("Product Category")
plt.ylabel("Sales (INR)")
plt.xticks(rotation=20)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig("outputs/task5/bar_chart.png", dpi=300)
plt.close()

print("2. Bar chart saved successfully!")

# 3. PIE CHART
region_sales = df.groupby("Region")["Sales_INR"].sum()

plt.figure(figsize=(7, 7))
plt.pie(
    region_sales.values,
    labels=region_sales.index,
    autopct="%1.1f%%",
    startangle=90
)
plt.title("Regional Share of Total Sales")
plt.tight_layout()

plt.savefig("outputs/task5/pie_chart.png", dpi=300)
plt.close()

print("3. Pie chart saved successfully!")

# 4. HISTOGRAM
plt.figure(figsize=(8, 5))
plt.hist(df["Sales_INR"].dropna(), bins=12, edgecolor="black")
plt.title("Distribution of Sales")
plt.xlabel("Sales (INR)")
plt.ylabel("Frequency")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()

plt.savefig("outputs/task5/histogram.png", dpi=300)
plt.close()

print("4. Histogram saved successfully!")

# 5. SCATTER PLOT
plt.figure(figsize=(8, 5))
plt.scatter(
    df["Units_Sold"],
    df["Sales_INR"],
    alpha=0.7,
    edgecolors="black"
)
plt.title("Units Sold vs Sales")
plt.xlabel("Units Sold")
plt.ylabel("Sales (INR)")
plt.grid(alpha=0.3)
plt.tight_layout()

plt.savefig("outputs/task5/scatter_plot.png", dpi=300)
plt.close()

print("5. Scatter plot saved successfully!")

print("\nAll 5 charts have been created!")
print("Check the outputs/task5 folder.")