import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# --------------------------------------------------
# 1. Setup
# --------------------------------------------------

OUTPUT_DIR = os.path.join("outputs", "task6")
DATA_PATH = os.path.join("data", "retail_sales_clean.csv")

os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set_theme(style="whitegrid")

print("=" * 55)
print("TASK 6: DATA VISUALIZATION USING SEABORN")
print("=" * 55)

# --------------------------------------------------
# 2. Load Dataset
# --------------------------------------------------

if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(
        "Cleaned dataset not found! Please run Task 7 first."
    )

df = pd.read_csv(DATA_PATH)

print("\nDataset loaded successfully!")
print(f"Total rows: {len(df)}")
print(f"Total columns: {len(df.columns)}")

# Convert numeric columns
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

required_columns = [
    "Category",
    "Units_Sold",
    "Unit_Price_INR",
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

# --------------------------------------------------
# 3. Count Plot
# --------------------------------------------------

print("\nGenerating Count Plot...")

count_data = df.dropna(subset=["Category"])

if not count_data.empty:
    plt.figure(figsize=(9, 5))

    sns.countplot(
        data=count_data,
        x="Category",
        hue="Category",
        order=count_data["Category"].value_counts().index,
        legend=False
    )

    plt.title(
        "Number of Orders by Product Category",
        fontsize=14
    )
    plt.xlabel("Product Category")
    plt.ylabel("Number of Orders")
    plt.xticks(rotation=20)
    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "count_plot.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Count plot saved successfully.")

# --------------------------------------------------
# 4. Box Plot
# --------------------------------------------------

print("Generating Box Plot...")

box_data = df.dropna(
    subset=["Category", "Sales_INR"]
)

if not box_data.empty:
    plt.figure(figsize=(9, 5))

    sns.boxplot(
        data=box_data,
        x="Category",
        y="Sales_INR",
        hue="Category",
        legend=False
    )

    plt.title(
        "Sales Distribution by Product Category",
        fontsize=14
    )
    plt.xlabel("Product Category")
    plt.ylabel("Sales (INR)")
    plt.xticks(rotation=20)
    plt.tight_layout()

    plt.savefig(
        os.path.join(OUTPUT_DIR, "box_plot.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Box plot saved successfully.")

# --------------------------------------------------
# 5. Correlation Heatmap
# --------------------------------------------------

print("Generating Correlation Heatmap...")

heatmap_data = df[numeric_columns].dropna()

if len(heatmap_data) >= 2:
    correlation_matrix = heatmap_data.corr()

    plt.figure(figsize=(10, 6))

    sns.heatmap(
        correlation_matrix,
        annot=True,
        cmap="coolwarm",
        fmt=".2f",
        linewidths=0.5
    )

    plt.title(
        "Correlation Heatmap of Retail Sales Data",
        fontsize=14
    )
    plt.tight_layout()

    plt.savefig(
        os.path.join(
            OUTPUT_DIR,
            "correlation_heatmap.png"
        ),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()

    print("Correlation heatmap saved successfully.")

else:
    print("Heatmap skipped: insufficient numeric data.")

# --------------------------------------------------
# 6. Pair Plot
# --------------------------------------------------

print("Generating Pair Plot...")

pair_columns = [
    "Units_Sold",
    "Unit_Price_INR",
    "Sales_INR",
    "Profit_INR"
]

pair_data = df[pair_columns].dropna()

if len(pair_data) >= 2:
    pair_plot = sns.pairplot(
        pair_data,
        diag_kind="hist"
    )

    pair_plot.fig.suptitle(
        "Pair Plot of Retail Sales Variables",
        y=1.02,
        fontsize=14
    )

    pair_plot.savefig(
        os.path.join(OUTPUT_DIR, "pair_plot.png"),
        dpi=300,
        bbox_inches="tight"
    )

    plt.close(pair_plot.fig)

    print("Pair plot saved successfully.")

else:
    print("Pair plot skipped: insufficient numeric data.")

# --------------------------------------------------
# 7. Final Status
# --------------------------------------------------

print("\n" + "=" * 55)
print("TASK 6 COMPLETED SUCCESSFULLY!")
print("=" * 55)

print("\nCheck the following output files:")

expected_files = [
    "count_plot.png",
    "box_plot.png",
    "correlation_heatmap.png",
    "pair_plot.png"
]

for filename in expected_files:
    file_path = os.path.join(OUTPUT_DIR, filename)

    if os.path.exists(file_path):
        print(f"[OK] {filename}")
    else:
        print(f"[NOT GENERATED] {filename}")

print(f"\nAll outputs are saved in: {OUTPUT_DIR}")