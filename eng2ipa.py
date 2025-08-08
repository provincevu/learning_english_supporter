import eng_to_ipa as ipa

def get_phonetics_for_phrases(phrases):
    """
    Nhận vào list các cụm từ (phrases), trả về dict với key là cụm từ,
    value là phiên âm IPA của cụm đó.
    """
    results = {}
    for phrase in phrases:
        ipa_text = ipa.convert(phrase)
        results[phrase] = ipa_text
    return results