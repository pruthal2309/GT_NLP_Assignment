import pandas as pd
import re

# Load dataset
df = pd.read_csv("data/sentences_dataset.csv")

def clean_sentence(sentence):
    
    # remove headings like ---- Properties ----
    if "----" in sentence:
        return None
    
    # remove references like [1], [2]
    if re.search(r"\[\d+\]", sentence):
        return None
    
    # remove urls
    if "http" in sentence:
        return None
    
    # remove weird encoding characters
    if re.search(r"[^\x00-\x7F]+", sentence):
        return None

    # remove extra spaces
    sentence = re.sub(r"\s+", " ", sentence)

    return sentence.strip()


cleaned_sentences = []

for _, row in df.iterrows():

    sentence = clean_sentence(row["sentence"])

    if sentence is not None:
        cleaned_sentences.append({
            "id": row["id"],
            "sentence": sentence,
            "source": row["source"],
            "length": len(sentence.split())
        })

clean_df = pd.DataFrame(cleaned_sentences)

# remove duplicates
clean_df = clean_df.drop_duplicates(subset=["sentence"])

# save cleaned dataset
clean_df.to_csv("data/clean_sentences_dataset.csv", index=False)

print("Clean dataset created.")
print("Total sentences:", len(clean_df))