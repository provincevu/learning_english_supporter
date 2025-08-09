import spacy

nlp = spacy.load("en_core_web_sm")

def extract_phrases(text):
    doc = nlp(text)
    phrase_spans = []

    # Lấy các cụm giới từ (prepositional phrases) trước
    prep_spans = []
    for token in doc:
        if token.pos_ == "ADP":
            subtree = list(token.subtree)
            start = subtree[0].i
            end = subtree[-1].i + 1
            phrase = doc[start:end].text
            prep_spans.append((start, end, phrase))
            phrase_spans.append((start, end, phrase))

    # Lấy các cụm danh từ (noun chunks), loại những cụm nằm hoàn toàn trong cụm giới từ
    for chunk in doc.noun_chunks:
        nc_start, nc_end = chunk.start, chunk.end
        # Nếu noun chunk nằm HOÀN TOÀN TRONG một prep span thì bỏ qua
        if any(nc_start >= p_start and nc_end <= p_end for p_start, p_end, _ in prep_spans):
            continue
        phrase_spans.append((nc_start, nc_end, chunk.text))

    # Lấy động từ chính (verbs)
    for token in doc:
        if token.pos_ == "VERB" and token.dep_ == "ROOT":
            start = token.i
            end = token.i + 1
            if not any(start == s and end == e for s, e, _ in phrase_spans):
                phrase_spans.append((start, end, token.text))

    # Sắp xếp theo vị trí xuất hiện trong câu
    phrase_spans.sort(key=lambda x: x[0])

    # Trả về list text của cụm đúng thứ tự
    return [text for _, _, text in phrase_spans]