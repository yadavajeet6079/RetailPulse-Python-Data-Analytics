import os
import numpy as np
import matplotlib.pyplot as plt
from statistics import mean, median, mode

# Dataset
data = [12, 15, 15, 18, 20, 22, 22, 22, 25, 29, 30]

# Statistical calculations
mean_value = mean(data)
median_value = median(data)
mode_value = mode(data)

# Display results
print("STATISTICAL ANALYSIS")
print("-" * 35)
print(f"Mean: {mean_value:.2f}")
print(f"Median: {median_value}")
print(f"Mode: {mode_value}")

# Explanation
print("\nINTERPRETATION")
print("-" * 35)
print("Mean represents the average value of the dataset.")
print("Median represents the middle value of the dataset.")
print("Mode represents the most frequently occurring value.")

# Create output folder automatically
output_dir = os.path.join("outputs", "task1")
os.makedirs(output_dir, exist_ok=True)

# Create histogram
plt.figure(figsize=(8, 5))
plt.hist(data, bins=6, edgecolor="black")

plt.title("Distribution of Data Values")
plt.xlabel("Values")
plt.ylabel("Frequency")
plt.grid(axis="y", linestyle="--", alpha=0.5)

plt.tight_layout()

# Save graph
output_path = os.path.join(output_dir, "task1_distribution.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")

print(f"\nGraph saved successfully at: {output_path}")

# Display graph
plt.show()