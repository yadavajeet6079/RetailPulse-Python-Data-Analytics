import os
import pandas as pd

# Load cleaned dataset
df = pd.read_csv("data/retail_sales_clean.csv")

# Create output folder
os.makedirs("outputs/task9", exist_ok=True)

print("=" * 55)
print("TASK 9: BUSINESS RECOMMENDATIONS")
print("=" * 55)

# Category performance
category_summary = (
    df.groupby("Category")
    .agg(
        Total_Sales=("Sales_INR", "sum"),
        Total_Profit=("Profit_INR", "sum"),
        Total_Units=("Units_Sold", "sum"),
        Order_Count=("Order_ID", "count")
    )
    .sort_values("Total_Sales", ascending=False)
)

# Regional performance
region_summary = (
    df.groupby("Region")
    .agg(
        Total_Sales=("Sales_INR", "sum"),
        Total_Profit=("Profit_INR", "sum"),
        Order_Count=("Order_ID", "count")
    )
    .sort_values("Total_Sales", ascending=False)
)

# Display category summary
print("\n1. CATEGORY PERFORMANCE")
print(category_summary.round(2).to_string())

# Display regional summary
print("\n2. REGIONAL PERFORMANCE")
print(region_summary.round(2).to_string())

# Identify highest-sales category and region
top_category = category_summary["Total_Sales"].idxmax()
top_region = region_summary["Total_Sales"].idxmax()

# Identify most profitable category
top_profit_category = category_summary["Total_Profit"].idxmax()

# Identify lowest-sales category and region
lowest_category = category_summary["Total_Sales"].idxmin()
lowest_region = region_summary["Total_Sales"].idxmin()

# Overall performance
total_sales = df["Sales_INR"].sum()
total_profit = df["Profit_INR"].sum()
total_orders = len(df)

print("\n3. OVERALL BUSINESS PERFORMANCE")
print(f"Total Sales: INR {total_sales:,.2f}")
print(f"Total Profit: INR {total_profit:,.2f}")
print(f"Total Orders: {total_orders}")

# Recommendations
recommendations = [
    (
        "Recommendation 1: Inventory Management",
        f"{top_category} generates the highest total sales. "
        "Review its stock levels regularly and maintain sufficient "
        "inventory to reduce the risk of stockouts."
    ),
    (
        "Recommendation 2: Regional Marketing",
        f"{top_region} generates the highest regional sales. "
        "Study its successful sales patterns and test whether "
        "similar marketing strategies work in other regions."
    ),
    (
        "Recommendation 3: Review Low-Performing Categories",
        f"{lowest_category} has the lowest total sales among the "
        "listed categories. Investigate demand, pricing, product "
        "availability and customer feedback before changing its inventory."
    ),
    (
        "Recommendation 4: Profitability Monitoring",
        f"{top_profit_category} has the highest total profit. "
        "Review its costs and margins to understand which practices "
        "could improve profitability in other categories."
    ),
    (
        "Recommendation 5: Regional Performance Review",
        f"{lowest_region} has the lowest regional sales. "
        "Investigate local demand, product availability and customer "
        "preferences before deciding on targeted promotions."
    )
]

print("\n" + "=" * 55)
print("4. DATA-DRIVEN BUSINESS RECOMMENDATIONS")
print("=" * 55)

for title, recommendation in recommendations:
    print(f"\n{title}")
    print(recommendation)

# Save reports
category_summary.to_csv(
    "outputs/task9/category_performance.csv"
)

region_summary.to_csv(
    "outputs/task9/region_performance.csv"
)

recommendation_df = pd.DataFrame(
    recommendations,
    columns=["Recommendation", "Details"]
)

recommendation_df.to_csv(
    "outputs/task9/business_recommendations.csv",
    index=False
)

print("\nReports saved in outputs/task9/")