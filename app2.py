from flask import Flask, render_template, request
from deep_translator import GoogleTranslator

app = Flask(__name__)

def extract_phrases(sentence):
    # Tách từng từ, hoặc bạn có thể thay bằng tách cụm thông minh hơn
    return sentence.strip().split()

def align_phrases(en_sentence, vi_sentence, phrases):
    vi_phrases = []
    # Dịch từng phrase để tìm vị trí nghĩa trong bản dịch câu
    phrase2vi = {}
    for ph in phrases:
        try:
            vi = GoogleTranslator(source='en', target='vi').translate(ph)
            if vi is None:
                vi = ""
        except Exception:
            vi = ""
        phrase2vi[ph] = vi

    vi_work = vi_sentence if vi_sentence else ""
    for idx, ph in enumerate(phrases):
        vi_mean = phrase2vi.get(ph, "")
        if not isinstance(vi_mean, str):
            vi_mean = ""
        start = vi_work.find(vi_mean) if vi_mean else -1
        if start != -1 and vi_mean.strip() != "":
            vi_phrases.append({
                "vi": vi_mean,
                "start": start,
                "end": start+len(vi_mean),
                "data_phrase": f"p{idx}"
            })
            vi_work = vi_work.replace(vi_mean, "*"*len(vi_mean), 1)
        else:
            vi_phrases.append({
                "vi": "",
                "start": -1,
                "end": -1,
                "data_phrase": f"p{idx}"
            })
    return vi_phrases, phrase2vi

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        sentence = request.form.get('sentence', '').strip()
        if not sentence:
            return render_template('trans.html', result=None)
        phrases = extract_phrases(sentence)
        vi_full = GoogleTranslator(source='en', target='vi').translate(sentence)
        vi_phrases, phrase2vi = align_phrases(sentence, vi_full, phrases)
        result = {
            "sentence": sentence,
            "phrases": [
                {
                    "text": phrase,
                    "vi_mean": phrase2vi.get(phrase, ""),
                    "data_phrase": f"p{i}"
                }
                for i, phrase in enumerate(phrases)
            ],
            "vi_full": vi_full,
            "vi_phrases": vi_phrases
        }
    return render_template('trans.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)