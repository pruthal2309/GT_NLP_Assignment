import spacy
import pandas as pd

# load spacy model
nlp = spacy.load("en_core_web_sm")

# load cleaned dataset
df = pd.read_csv("data/clean_sentences_dataset.csv")

parsed_rows = []

for _, row in df.iterrows():

    sentence = row["sentence"]
    doc = nlp(sentence)

    for token in doc:

        parsed_rows.append({
            "sentence_id": row["id"],
            "word": token.text,
            "dependency": token.dep_,
            "head": token.head.text
        })

parse_df = pd.DataFrame(parsed_rows)

parse_df.to_csv("data/dependency_parse.csv", index=False)

print("Dependency parsing completed")