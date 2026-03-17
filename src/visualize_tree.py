import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import string

#
# ---------- Tree Layout Function ----------
def hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0):

    def _hierarchy_pos(G, root, left, right, vert_loc, pos, visited):
        if root in visited:
            return pos
        visited.add(root) 

        pos[root] = ((left + right) / 2, vert_loc)
        children = list(G.successors(root))

        if children:
            dx = (right - left) / len(children)
            nextx = left
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(
                    G, child, nextx - dx, nextx,
                    vert_loc - vert_gap, pos, visited
                )
        return pos

    return _hierarchy_pos(G, root, 0, width, vert_loc, {}, set())


# ---------- Load Dependency Data ----------
df = pd.read_csv("data/dependency_parse.csv")
sentence_ids = df["sentence_id"].unique()[:5]

for sentence_id in sentence_ids:
    sentence_data = df[df["sentence_id"] == sentence_id].reset_index(drop=True)

    # ---------- Build Graph with unique node IDs ----------
    G = nx.DiGraph()
    nodes_by_pos = {}

    for idx, row in sentence_data.iterrows():
        word = str(row["word"]).strip()
        head = str(row["head"]).strip() if pd.notna(row["head"]) else None

        # Skip punctuation
        if word in string.punctuation:
            continue

        nodes_by_pos[idx] = {
            "word": word,
            "head": head,
            "node_id": f"{word}_{idx}"
        }

    # Add all valid nodes first
    for idx, data in nodes_by_pos.items():
        G.add_node(data["node_id"])

    # Detect root and add edges
    root_node = None
    sentence_words = {d["word"]: d["node_id"] for d in nodes_by_pos.values()}

    for idx, data in nodes_by_pos.items():
        word = data["word"]
        head = data["head"]
        node_id = data["node_id"]

        is_root = (head is None) or (head == word) or (head not in sentence_words)
        if is_root:
            if root_node is None:
                root_node = node_id
            continue

        head_node = sentence_words[head]
        if head_node != node_id:
            G.add_edge(head_node, node_id)

    if root_node is None:
        print(f"Skipping sentence {sentence_id}: no root found.")
        continue

    # ---------- Break cycles ----------
    try:
        cycles = list(nx.simple_cycles(G))
        for cycle in cycles:
            G.remove_edge(cycle[-1], cycle[0])
            print(f"  Removed cycle edge: {cycle[-1]} → {cycle[0]}")
    except Exception as e:
        print(f"Cycle check failed: {e}")

    # ---------- Keep only nodes reachable from root ----------
    reachable = nx.descendants(G, root_node) | {root_node}
    nodes_to_remove = [n for n in list(G.nodes()) if n not in reachable]
    if nodes_to_remove:
        print(f"  Sentence {sentence_id}: removing {len(nodes_to_remove)} unreachable node(s): {nodes_to_remove}")
    G.remove_nodes_from(nodes_to_remove)

    # ---------- Compute Layout ----------
    try:
        pos = hierarchy_pos(G, root_node)
    except Exception as e:
        print(f"Layout failed for sentence {sentence_id}: {e}")
        continue

    # Verify all nodes have positions (safety check)
    missing = [n for n in G.nodes() if n not in pos]
    if missing:
        print(f"  Warning: {len(missing)} node(s) still missing positions, skipping.")
        continue

    # Clean display labels: strip the _index suffix
    labels = {node: node.rsplit("_", 1)[0] for node in G.nodes()}

    # ---------- Draw ----------
    plt.figure(figsize=(12, 7))
    nx.draw(
        G, pos,
        labels=labels,
        with_labels=True,
        node_size=2500,
        node_color="lightblue",
        font_size=10,
        arrows=True
    )
    plt.title(f"Dependency Parse Tree — Sentence {sentence_id}")
    plt.subplots_adjust(top=0.9)
    plt.show()