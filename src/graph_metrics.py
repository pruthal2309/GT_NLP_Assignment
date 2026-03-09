import pandas as pd
import networkx as nx

df = pd.read_csv("data/dependency_parse.csv")

metrics = []

for sentence_id in df["sentence_id"].unique():

    sentence_data = df[df["sentence_id"] == sentence_id]

    G = nx.DiGraph()

    for _, row in sentence_data.iterrows():

        if row["head"] != row["word"]:
            G.add_edge(row["head"], row["word"])

    metrics.append({
        "sentence_id": sentence_id,
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "avg_degree": sum(dict(G.degree()).values()) / G.number_of_nodes()
    })

metrics_df = pd.DataFrame(metrics)

metrics_df.to_csv("data/graph_metrics.csv", index=False)

print("Graph metrics computed")