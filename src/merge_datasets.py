import pandas as pd

# Load datasets
graph_df = pd.read_csv("src/data/graph_metrics.csv")
readability_df = pd.read_csv("src/data/readability_scores.csv")

# Merge using sentence_id
merged_df = pd.merge(
    graph_df,
    readability_df,
    on="sentence_id",
    how="inner"
)

# Save final dataset
merged_df.to_csv("src/data/final_analysis_dataset.csv", index=False)

print("Datasets merged successfully")
print("Total rows:", len(merged_df))

print("\nColumns in final dataset:")
print(merged_df.columns)