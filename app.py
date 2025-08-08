from flask import Flask, render_template, request, jsonify
from phrase_extractor import extract_phrases
from eng2ipa import get_phonetics_for_phrases
from trans import translate_phrases

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        sentence = request.form.get("sentence", "").strip()
        phrases = extract_phrases(sentence)
        ipa_dict = get_phonetics_for_phrases(phrases)
        trans_dict = translate_phrases(phrases, dest='vi')
        result = {
            "sentence": sentence,
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

# API endpoint cho JS fetch
@app.route('/api/phrase-ipa', methods=['POST'])
def api_phrase_ipa():
    data = request.get_json()
    sentence = data.get("sentence", "")
    phrases = extract_phrases(sentence)
    ipa_dict = get_phonetics_for_phrases(phrases)
    trans_dict = translate_phrases(phrases, dest='vi')
    return jsonify({
        "phrases": [
            {
                "text": phrase,
                "ipa": ipa_dict.get(phrase, ""),
                "vi": trans_dict.get(phrase, "")
            }
            for phrase in phrases
        ]
    })

# Route đọc file input.txt và show kết quả cho nhiều câu
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
    for sentence in sentences:
        phrases = extract_phrases(sentence)
        ipa_dict = get_phonetics_for_phrases(phrases)
        trans_dict = translate_phrases(phrases, dest='vi')
        batch_results.append({
            "sentence": sentence,
            "phrases": [
                {
                    "text": phrase,
                    "ipa": ipa_dict.get(phrase, ""),
                    "vi": trans_dict.get(phrase, "")
                }
                for phrase in phrases
            ]
        })
    return render_template('batch.html', batch_results=batch_results)

if __name__ == '__main__':
    app.run(debug=True)