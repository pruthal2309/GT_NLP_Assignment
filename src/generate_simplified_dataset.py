import pandas as pd
from sentence_simplification import simplify_sentence

df = pd.read_csv("data/clean_sentences_dataset.csv")

simplified = []

for sentence in df["sentence"]:
    simple = simplify_sentence(sentence)
    simplified.append(simple)

df["simplified_sentence"] = simplified

df.to_csv("data/simplified_sentences.csv", index=False)

print("Simplified dataset created.")