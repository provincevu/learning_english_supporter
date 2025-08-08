from googletrans import Translator

translator = Translator()

def translate_phrases(phrases, dest='vi'):
    result = {}
    try:
        translations = translator.translate(phrases, dest=dest)
        # Nếu phrases là list nhiều phần tử
        if isinstance(translations, list):
            for phrase, trans in zip(phrases, translations):
                result[phrase] = trans.text
        else:
            # Nếu chỉ là 1 chuỗi
            result[phrases] = translations.text
    except Exception as e:
        print(f"Lỗi dịch googletrans: {e}")
        # Trả về chuỗi báo lỗi cho từng phrase, tránh app sập
        if isinstance(phrases, list):
            for phrase in phrases:
                result[phrase] = "Dịch lỗi"
        else:
            result[phrases] = "Dịch lỗi"
    return result