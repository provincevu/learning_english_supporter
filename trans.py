from googletrans import Translator

def translate_phrases(phrases, dest='vi'):
    """
    Dịch các cụm từ sang ngôn ngữ đích (mặc định là tiếng Việt).
    phrases: list các cụm từ tiếng Anh (str)
    dest: mã ngôn ngữ đích (vd: 'vi' cho tiếng Việt)
    Trả về dict {phrase: translation}
    """
    translator = Translator()
    result = {}
    # googletrans dịch batch hiệu quả hơn
    translations = translator.translate(phrases, dest=dest)
    for src, trans in zip(phrases, translations):
        result[src] = trans.text
    return result

if __name__ == "__main__":
    test_phrases = ["Replace", "shell scripts", "under this directory", "to", "original ones"]
    trans = translate_phrases(test_phrases)
    print(trans)