import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load merged dataset
df = pd.read_csv("src/data/final_analysis_dataset.csv")

print("Dataset Loaded")
print(df.head())


# ------------------------------
# Correlation Matrix
# ------------------------------

correlation = df.corr(numeric_only=True)

print("\nCorrelation Matrix:")
print(correlation)

plt.figure(figsize=(8,6))

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm"
)

plt.title("Correlation Between Graph Metrics and Readability")

plt.show()


# ------------------------------
# Scatter Plot 1
# Nodes vs Readability
# ------------------------------

plt.figure(figsize=(7,5))

sns.scatterplot(
    x="nodes",
    y="flesch_reading_ease",
    data=df
)

plt.title("Nodes vs Flesch Reading Ease")

plt.show()


# ------------------------------
# Scatter Plot 2
# Sentence Length vs Readability
# ------------------------------

plt.figure(figsize=(7,5))

sns.scatterplot(
    x="length",
    y="flesch_kincaid_grade",
    data=df
)

plt.title("Sentence Length vs Grade Level")

plt.show()


# ------------------------------
# Distribution Plot
# ------------------------------

plt.figure(figsize=(7,5))

sns.histplot(
    df["flesch_reading_ease"],
    bins=20,
    kde=True
)

plt.title("Distribution of Readability Scores")

plt.show()


print("Statistical analysis completed")