import os
import numpy as np
import matplotlib.pyplot as plt

# Dataset
data = [18, 20, 21, 22, 22, 24, 25, 27, 29, 32]

# Statistical calculations
mean_value = np.mean(data)
population_variance = np.var(data)
population_std = np.std(data)

sample_variance = np.var(data, ddof=1)
sample_std = np.std(data, ddof=1)

# Display results
print("VARIANCE AND STANDARD DEVIATION")
print("-" * 40)

print(f"Mean: {mean_value:.2f}")
print(f"Population Variance: {population_variance:.2f}")
print(f"Population Standard Deviation: {population_std:.2f}")
print(f"Sample Variance: {sample_variance:.2f}")
print(f"Sample Standard Deviation: {sample_std:.2f}")

print("\nINTERPRETATION")
print("-" * 40)
print("Variance measures how widely the values are spread.")
print("Standard deviation shows the spread in the original units.")
print("A higher standard deviation indicates greater variability.")

# Create output folder
os.makedirs("outputs/task2", exist_ok=True)

# Create graph
plt.figure(figsize=(8, 5))
plt.hist(data, bins=6, edgecolor="black")

plt.axvline(
    mean_value,
    linestyle="--",
    linewidth=2,
    label=f"Mean = {mean_value:.2f}"
)

plt.title("Distribution and Spread of Data")
plt.xlabel("Values")
plt.ylabel("Frequency")
plt.legend()
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()
plt.savefig(
    "outputs/task2/task2_variance.png",
    dpi=300,
    bbox_inches="tight"
)

print("\nGraph saved: outputs/task2/task2_variance.png")

plt.show()