from flask import Flask, render_template, request, jsonify, Response
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

def dedup_phrases_keep_underscore(phrases):
    """
    Giữ nguyên các cụm chỉ gồm dấu "_" (hoặc "__", "___"...), 
    các cụm khác thì chỉ giữ lần xuất hiện đầu tiên (không lặp lại).
    """
    seen = set()
    result = []
    for phrase in phrases:
        clean = phrase.strip()
        if clean and all(c == '_' for c in clean):
            # Cụm toàn dấu _ giữ nguyên, không loại lặp
            result.append(phrase)
        elif clean not in seen:
            result.append(phrase)
            seen.add(clean)
    return result

@app.route('/batch_stream')
def batch_stream():
    def generate():
        try:
            with open('input.txt', encoding='utf-8') as f:
                for idx, line in enumerate(f, 1):
                    sentence = line.strip()
                    if not sentence:
                        continue
                    phrases = extract_phrases(sentence)
                    phrases_dedup = dedup_phrases_keep_underscore(phrases)
                    ipa_dict = get_phonetics_for_phrases(phrases)
                    trans_dict = translate_phrases(phrases, dest='vi')
                    vi_full = translate_sentence(sentence, dest='vi')
                    vi_phrase_spans = [
                        {
                            "vi": trans_dict.get(phrase, ""),
                            "data_phrase": f"{idx}-{i+1}"
                        }
                        for i, phrase in enumerate(phrases)
                    ]
                    data = {
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
                        ],
                        "phrases_dedup": [
                            {
                                "text": phrase,
                                # note: mapping to original index for hover if needed
                                "data_phrase": f"{idx}-{phrases.index(phrase)+1}"
                            }
                            for phrase in phrases_dedup
                        ],
                        "index": idx
                    }
                    import json
                    yield f"data: {json.dumps(data)}\n\n"
        except Exception as e:
            import json
            yield f"data: {json.dumps({'error': str(e)})}\n\n"
    return Response(generate(), mimetype='text/event-stream')

@app.route('/batch_progressive')
def batch_progressive():
    return render_template('batch_stream.html')

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
        phrases_dedup = dedup_phrases_keep_underscore(phrases)
        ipa_dict = get_phonetics_for_phrases(phrases)
        trans_dict = translate_phrases(phrases, dest='vi')
        vi_full = translate_sentence(sentence, dest='vi')
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
            ],
            "phrases_dedup": [
                {
                    "text": phrase,
                    "data_phrase": f"{idx}-{phrases.index(phrase)+1}"
                }
                for phrase in phrases_dedup
            ]
        })
    return render_template('batch.html', batch_results=batch_results)

if __name__ == '__main__':
    app.run(debug=True)