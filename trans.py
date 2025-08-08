from deep_translator import GoogleTranslator

def translate_phrases(phrases, dest='vi'):
    result = {}
    for phrase in phrases:
        try:
            vi = GoogleTranslator(source='en', target=dest).translate(phrase)
        except Exception as e:
            print(f"Lỗi dịch: {e}")
            vi = "Dịch lỗi"
        result[phrase] = vi
    return result

def translate_sentence(sentence, dest='vi'):
    try:
        return GoogleTranslator(source='en', target=dest).translate(sentence)
    except Exception as e:
        print(f"Lỗi dịch cả câu: {e}")
        return "Dịch lỗi"