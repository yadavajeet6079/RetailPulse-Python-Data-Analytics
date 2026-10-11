import os
import pandas as pd
import matplotlib.pyplot as plt

# Load cleaned dataset
df = pd.read_csv("data/retail_sales_clean.csv")

# Create output folder
os.makedirs("outputs/task3", exist_ok=True)

# Select variables
x = df["Units_Sold"]
y = df["Sales_INR"]

# Calculate correlation
correlation = x.corr(y)

print("=" * 45)
print("TASK 3: CORRELATION AND PROBABILITY")
print("=" * 45)

print(f"\nCorrelation between Units Sold and Sales: {correlation:.3f}")

if correlation >= 0.7:
    print("Interpretation: Strong positive correlation.")
elif correlation >= 0.3:
    print("Interpretation: Moderate positive correlation.")
elif correlation > -0.3:
    print("Interpretation: Weak linear correlation.")
elif correlation > -0.7:
    print("Interpretation: Moderate negative correlation.")
else:
    print("Interpretation: Strong negative correlation.")

# Scatter plot
plt.figure(figsize=(8, 5))
plt.scatter(x, y, alpha=0.7, edgecolors="black")

plt.title("Relationship Between Units Sold and Sales")
plt.xlabel("Units Sold")
plt.ylabel("Sales (INR)")
plt.grid(alpha=0.3)

plt.tight_layout()
plt.savefig(
    "outputs/task3/task3_correlation.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nGraph saved: outputs/task3/task3_correlation.png")

# Simple probability example:
# Probability that a randomly selected order is from the Electronics category
total_orders = len(df)
electronics_orders = (df["Category"] == "Electronics").sum()

if total_orders > 0:
    probability = electronics_orders / total_orders

    print("\nPROBABILITY EXAMPLE")
    print(f"Total orders: {total_orders}")
    print(f"Electronics orders: {electronics_orders}")
    print(f"Probability: {probability:.2%}")
else:
    print("Dataset contains no orders.")

plt.show()