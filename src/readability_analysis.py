import pandas as pd
import textstat

# Load cleaned dataset
df = pd.read_csv("src/data/clean_sentences_dataset.csv")

results = []

for _, row in df.iterrows():

    sentence = row["sentence"]
    sentence_id = row["id"]

    flesch_score = textstat.flesch_reading_ease(sentence)

    grade_level = textstat.flesch_kincaid_grade(sentence)

    results.append({
        "sentence_id": sentence_id,
        "sentence": sentence,
        "length": len(sentence.split()),
        "flesch_reading_ease": flesch_score,
        "flesch_kincaid_grade": grade_level
    })

readability_df = pd.DataFrame(results)

# Save results
readability_df.to_csv("src/data/readability_scores.csv", index=False)

print("Readability analysis completed")
print("Total sentences analyzed:", len(readability_df))