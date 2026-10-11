import os
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv("data/retail_sales_clean.csv")

# Create output folder
os.makedirs("outputs/task4", exist_ok=True)

# Select column for outlier detection
column = "Sales_INR"
data = df[column].dropna()

# Calculate quartiles
Q1 = data.quantile(0.25)
Q3 = data.quantile(0.75)

IQR = Q3 - Q1

# Calculate outlier limits
lower_limit = Q1 - 1.5 * IQR
upper_limit = Q3 + 1.5 * IQR

# Identify outliers
outliers = df[
    (df[column] < lower_limit)
    | (df[column] > upper_limit)
].copy()

print("=" * 45)
print("TASK 4: OUTLIER DETECTION")
print("=" * 45)

print(f"\nQ1: {Q1:.2f}")
print(f"Q3: {Q3:.2f}")
print(f"IQR: {IQR:.2f}")
print(f"Lower limit: {lower_limit:.2f}")
print(f"Upper limit: {upper_limit:.2f}")

print(f"\nNumber of outliers: {len(outliers)}")

if outliers.empty:
    print("No outliers were detected using the IQR method.")
else:
    print("\nDetected outlier records:")
    print(outliers[["Order_ID", "Category", "Sales_INR"]].to_string(index=False))

# Save outliers
outliers.to_csv(
    "outputs/task4/task4_outliers.csv",
    index=False
)

# Create box plot
plt.figure(figsize=(8, 5))
plt.boxplot(data, vert=True)

plt.title("Box Plot of Sales: Outlier Detection")
plt.ylabel("Sales (INR)")
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(
    "outputs/task4/task4_boxplot.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nOutlier records saved: outputs/task4/task4_outliers.csv")
print("Box plot saved: outputs/task4/task4_boxplot.png")

print("\nINTERPRETATION")
print("Outliers are values outside the IQR-based limits.")
print("They may affect averages, charts, and business decisions.")
print("An outlier should be investigated before removing it.")

plt.show()