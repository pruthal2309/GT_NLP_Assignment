import pandas as pd
import networkx as nx

df = pd.read_csv("data/dependency_parse.csv")

graphs = {}

for sentence_id in df["sentence_id"].unique():

    sentence_data = df[df["sentence_id"] == sentence_id]

    G = nx.DiGraph()

    for _, row in sentence_data.iterrows():

        head = row["head"]
        word = row["word"]

        if head != word:
            G.add_edge(head, word)

    graphs[sentence_id] = G

print("Graphs created:", len(graphs))