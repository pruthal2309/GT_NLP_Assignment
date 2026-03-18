import spacy

nlp = spacy.load("en_core_web_sm")

def simplify_sentence(sentence):
    doc = nlp(sentence)

    simplified_tokens = []

    for token in doc:
        # remove punctuation
        if token.pos_ == "PUNCT":
            continue
        
        # remove some modifiers
        if token.dep_ in ["amod", "advmod"]:
            continue
        
        simplified_tokens.append(token.text)

    simplified_sentence = " ".join(simplified_tokens)

    return simplified_sentence


if __name__ == "__main__":
    sentence = "The committee, after reviewing the proposals submitted last month, decided to postpone the decision."
    
    simple = simplify_sentence(sentence)

    print("Original:", sentence)
    print("Simplified:", simple)