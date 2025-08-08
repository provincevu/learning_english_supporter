import spacy

# Chỉ load nlp 1 lần khi file được import
nlp = spacy.load("en_core_web_sm")

def extract_phrases(text):
    doc = nlp(text)
    phrases = []

    # Lấy các cụm danh từ (noun chunks)
    for chunk in doc.noun_chunks:
        phrases.append(chunk.text)

    # Lấy các cụm giới từ (prepositional phrases)
    for token in doc:
        if token.pos_ == "ADP":
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            phrase = doc[start:end].text
            if phrase not in phrases:
                phrases.append(phrase)

    # Lấy các động từ chính (verbs)
    for token in doc:
        if token.pos_ == "VERB" and token.dep_ == "ROOT":
            if token.text not in phrases:
                phrases.insert(0, token.text)  # Đưa động từ lên đầu

    return phrases