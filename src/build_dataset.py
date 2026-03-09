import warnings
warnings.filterwarnings("ignore")
import wikipedia
import nltk
import pandas as pd
import os

# topics = [
#     "Graph theory",
#     "Artificial intelligence",
#     "Machine learning",
#     "Computer network",
#     "Algorithm",
#     "Data structure",
#     "Internet",
#     "Probability",
#     "Statistics",
#     "Neural network"
# ]
topics = [
    "Dog",
    "Cat",
    "Tree",
    "River",
    "Mountain",
    "Bird",
    "Sun",
    "Rain",
    "Forest",
    "Ocean"
]

sentences = []
id_counter = 1
max_per_topic = 50

for topic in topics:
    
    try:
        
        page = wikipedia.page(topic)
        text = page.content

        # split into sentences
        sent_list = nltk.sent_tokenize(text)

        count = 0
        for s in sent_list:
            word_count = len(s.split())

            # keep only clean sentences
            if 5 <= word_count <= 25:
                sentences.append({
                    "id": id_counter,
                    "sentence": s,
                    "source": topic,
                    "length": word_count
                })
                id_counter += 1
                count += 1

            if count >= max_per_topic:
                break
            
            if id_counter > 500:
                break

    except:
        continue

dataset = pd.DataFrame(sentences)

os.makedirs("data", exist_ok=True)
dataset.to_csv("data/sentences_dataset.csv", index=False)

print("Dataset created with", len(dataset), "sentences")