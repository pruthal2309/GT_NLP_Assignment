import pandas as pd
import networkx as nx

df = pd.read_csv("src/data/dependency_parse.csv")

metrics = []

for sentence_id in df["sentence_id"].unique():

    sentence_data = df[df["sentence_id"] == sentence_id]

    G = nx.DiGraph()

    for _, row in sentence_data.iterrows():

        if row["head"] != row["word"]:
            G.add_edge(row["head"], row["word"])

    nodes = G.number_of_nodes()
    edges = G.number_of_edges()

    leaf_nodes = len([n for n in G.nodes() if G.out_degree(n) == 0])

    branching_factor = sum(dict(G.out_degree()).values()) / nodes if nodes else 0

    root_nodes = [n for n in G.nodes() if G.in_degree(n) == 0]

    height = 0
    if root_nodes:
        root = root_nodes[0]
        lengths = nx.single_source_shortest_path_length(G, root)
        height = max(lengths.values())

    avg_dep_distance = 0
    if "token_id" in sentence_data.columns and "head_id" in sentence_data.columns:
        avg_dep_distance = (sentence_data["token_id"] - sentence_data["head_id"]).abs().mean()

    metrics.append({
        "sentence_id": sentence_id,
        "nodes": nodes,
        "edges": edges,
        "tree_height": height,
        "leaf_nodes": leaf_nodes,
        "branching_factor": branching_factor,
        "avg_dependency_distance": avg_dep_distance
    })

metrics_df = pd.DataFrame(metrics)

metrics_df.to_csv("src/data/graph_metrics.csv", index=False)

print("Graph metrics computed")