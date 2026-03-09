# Graph Theory + NLP Project Task Tracker

**Project:** Graph Properties of Parse Trees
**Goal:** Analyze dependency trees of sentences using graph theory metrics and correlate them with readability/complexity.

---

# Project Pipeline Overview

Sentence Dataset
→ Cleaning
→ Dependency Parsing
→ Graph Construction
→ Graph Visualization
→ Graph Metrics Extraction
→ Statistical Analysis
→ Correlation with Readability
→ Final Report

---

# Phase 1 — Dataset Creation

## Task 1.1 — Collect Sentence Dataset

Status: **Completed**

Description:
Collected sentences automatically from Wikipedia topics using Python.

Implementation:

* Used `wikipedia` Python library
* Extracted article text
* Split text into sentences using NLTK tokenizer
* Filtered sentences based on length

Output:

```
data/sentences_dataset.csv
```

Columns:

| Column   | Meaning             |
| -------- | ------------------- |
| id       | sentence identifier |
| sentence | extracted sentence  |
| source   | topic source        |
| length   | word count          |

Result:

* Initial dataset created successfully.

---

## Task 1.2 — Sentence Cleaning

Status: **Completed**

Description:
Removed noisy or invalid sentences.

Cleaning rules applied:

* Removed headings
* Removed reference markers `[1]`
* Removed URLs
* Removed encoding artifacts
* Removed duplicate sentences

Script:

```
src/clean_dataset.py
```

Output:

```
data/clean_sentences_dataset.csv
```

Result:

* Clean dataset generated
* Total sentences: **220**

---

# Phase 2 — Dependency Parsing

## Task 2.1 — Install NLP Parser

Status: **Completed**

Tools used:

* spaCy
* English model `en_core_web_sm`

Commands used:

```
pip install spacy
python -m spacy download en_core_web_sm
```

---

## Task 2.2 — Parse Sentences

Status: **Completed**

Description:
Each sentence converted into a dependency structure.

Implementation:

```
Sentence → spaCy Parser → Dependency relations
```

Script:

```
src/parse_sentences.py
```

Output file:

```
data/dependency_parse.csv
```

Columns:

| Column      | Meaning              |
| ----------- | -------------------- |
| sentence_id | sentence identifier  |
| word        | token                |
| dependency  | grammatical relation |
| head        | parent word          |

Result:

* Dependency relations extracted for all sentences.

---

# Phase 3 — Graph Construction

## Task 3.1 — Convert Dependency Trees to Graphs

Status: **Completed**

Description:

Dependency relations converted into directed graphs.

Graph structure:

```
head → word
```

Library used:

```
networkx
```

Graph type:

```
Directed graph (DiGraph)
```

Result:
Each sentence now corresponds to a **graph representation**.

---

# Phase 4 — Tree Visualization

## Task 4.1 — Dependency Tree Visualization

Status: **Completed**

Script:

```
src/visualize_tree.py
```

Features implemented:

* Hierarchical tree layout
* Root node detection
* Punctuation removal
* Directed edges

Visualization library:

```
matplotlib
```

Example output:

```
Dependency Parse Tree (Sentence ID X)
```

Purpose:

* Verify parsing correctness
* Include diagrams in project report

Note:
Only **5 sample trees** visualized to avoid opening hundreds of windows.

---

# Phase 5 — Graph Validation

## Task 5.1 — Cycle Detection

Status: **Completed**

Description:

Ensured graphs remain valid trees.

Checks added:

```
nx.is_directed_acyclic_graph(G)
```

Purpose:

Avoid recursion errors in visualization.

---

# Phase 6 — Graph Metrics Extraction

Status: **Pending**

Goal:
Compute graph-theoretic properties for each sentence tree.

Metrics to compute:

| Metric                  | Meaning                |
| ----------------------- | ---------------------- |
| Nodes                   | number of words        |
| Edges                   | number of dependencies |
| Tree height             | maximum root distance  |
| Leaf nodes              | pendant vertices       |
| Branching factor        | children per node      |
| Avg dependency distance | syntactic complexity   |

Script to create:

```
src/graph_metrics.py
```

Expected output:

```
data/graph_metrics.csv
```

---

# Phase 7 — Readability Analysis

Status: **Pending**

Goal:
Measure sentence difficulty.

Metrics:

* Flesch Reading Ease
* Flesch-Kincaid Grade Level
* sentence length

Library:

```
textstat
```

Script:

```
src/readability_analysis.py
```

Output:

```
data/readability_scores.csv
```

---

# Phase 8 — Dataset Integration

Status: **Pending**

Goal:

Merge:

```
Graph metrics + readability scores
```

Output:

```
data/final_analysis_dataset.csv
```

Example structure:

| sentence_id | nodes | height | branching | readability |

---

# Phase 9 — Statistical Analysis

Status: **Pending**

Goal:

Find relationships between graph structure and readability.

Methods:

* Pearson correlation
* Spearman correlation
* distribution plots

Tools:

```
pandas
matplotlib
seaborn
```

Output:

* scatter plots
* correlation matrix

---

# Phase 10 — Visualization & Results

Status: **Pending**

Graphs to generate:

* tree height vs readability
* branching factor distribution
* sentence complexity distribution

Saved in:

```
results/
```

---

# Phase 11 — Final Report

Status: **Pending**

Report sections:

1. Introduction
2. Dataset Description
3. Methodology
4. Graph Theory Concepts
5. Experiments
6. Results
7. Discussion
8. Conclusion

---

# Current Project Status

| Phase                    | Status    |
| ------------------------ | --------- |
| Dataset creation         | Completed |
| Dataset cleaning         | Completed |
| Dependency parsing       | Completed |
| Graph construction       | Completed |
| Tree visualization       | Completed |
| Graph metrics extraction | Pending   |
| Readability analysis     | Pending   |
| Correlation study        | Pending   |
| Final report             | Pending   |

---

# Immediate Next Task

Implement:

```
src/graph_metrics.py
```

Goal:

Automatically compute graph properties for all **220 sentence trees**.

---

# End of Task Tracker
