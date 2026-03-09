import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load final dataset
df = pd.read_csv("data/final_analysis_dataset.csv")

print("Dataset Loaded:", len(df), "sentences")


# -----------------------------
# Plot 1 — Tree Size vs Readability
# -----------------------------

plt.figure(figsize=(8,6))

sns.regplot(
    x="nodes",
    y="flesch_reading_ease",
    data=df,
    scatter_kws={"alpha":0.6}
)

plt.title("Tree Size vs Readability")
plt.xlabel("Number of Nodes in Parse Tree")
plt.ylabel("Flesch Reading Ease")

plt.savefig("data/tree_size_vs_readability.png")
plt.show()


# -----------------------------
# Plot 2 — Sentence Length vs Grade Level
# -----------------------------

plt.figure(figsize=(8,6))

sns.regplot(
    x="length",
    y="flesch_kincaid_grade",
    data=df,
    scatter_kws={"alpha":0.6}
)

plt.title("Sentence Length vs Reading Grade Level")

plt.savefig("data/length_vs_grade.png")
plt.show()


# -----------------------------
# Plot 3 — Graph Metric Distribution
# -----------------------------

plt.figure(figsize=(8,6))

sns.histplot(df["nodes"], bins=15, kde=True)

plt.title("Distribution of Parse Tree Sizes")

plt.xlabel("Number of Nodes")

plt.savefig("data/tree_size_distribution.png")
plt.show()


# -----------------------------
# Plot 4 — Readability Distribution
# -----------------------------

plt.figure(figsize=(8,6))

sns.histplot(df["flesch_reading_ease"], bins=20, kde=True)

plt.title("Distribution of Readability Scores")

plt.xlabel("Flesch Reading Ease")

plt.savefig("data/readability_distribution.png")
plt.show()


print("Final visualizations generated.")