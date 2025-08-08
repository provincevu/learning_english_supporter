from flask import Flask, render_template, request, jsonify
from phrase_extractor import extract_phrases
from eng2ipa import get_phonetics_for_phrases
from trans import translate_phrases, translate_sentence  # Thêm hàm dịch cả câu

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        sentence = request.form.get("sentence", "").strip()
        phrases = extract_phrases(sentence)
        ipa_dict = get_phonetics_for_phrases(phrases)
        trans_dict = translate_phrases(phrases, dest='vi')
        vi_full = translate_sentence(sentence, dest='vi')  # Dịch cả câu
        result = {
            "sentence": sentence,
            "vi_full": vi_full,
            "phrases": [
                {
                    "text": phrase,
                    "ipa": ipa_dict.get(phrase, ""),
                    "vi": trans_dict.get(phrase, "")
                }
                for phrase in phrases
            ]
        }
    return render_template('index.html', result=result)

@app.route('/api/phrase-ipa', methods=['POST'])
def api_phrase_ipa():
    data = request.get_json()
    sentence = data.get("sentence", "")
    phrases = extract_phrases(sentence)
    ipa_dict = get_phonetics_for_phrases(phrases)
    trans_dict = translate_phrases(phrases, dest='vi')
    vi_full = translate_sentence(sentence, dest='vi')
    return jsonify({
        "vi_full": vi_full,
        "phrases": [
            {
                "text": phrase,
                "ipa": ipa_dict.get(phrase, ""),
                "vi": trans_dict.get(phrase, "")
            }
            for phrase in phrases
        ]
    })

@app.route('/batch')
def batch():
    sentences = []
    try:
        with open('input.txt', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line:
                    sentences.append(line)
    except Exception as e:
        return f"Không đọc được file input.txt: {e}"

    batch_results = []
    for idx, sentence in enumerate(sentences, 1):
        phrases = extract_phrases(sentence)
        ipa_dict = get_phonetics_for_phrases(phrases)
        trans_dict = translate_phrases(phrases, dest='vi')
        vi_full = translate_sentence(sentence, dest='vi')
        # Dịch từng cụm - dùng để hover cụm trong bản dịch hoàn chỉnh
        vi_phrase_spans = [
            {
                "vi": trans_dict.get(phrase, ""),
                "data_phrase": f"{idx}-{i+1}"
            }
            for i, phrase in enumerate(phrases)
        ]
        batch_results.append({
            "sentence": sentence,
            "vi_full": vi_full,
            "vi_phrase_spans": vi_phrase_spans,
            "phrases": [
                {
                    "text": phrase,
                    "ipa": ipa_dict.get(phrase, ""),
                    "vi": trans_dict.get(phrase, ""),
                    "data_phrase": f"{idx}-{i+1}"
                }
                for i, phrase in enumerate(phrases)
            ]
        })
    return render_template('batch.html', batch_results=batch_results)

if __name__ == '__main__':
    app.run(debug=True)