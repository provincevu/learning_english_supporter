## Cài đặt nhanh môi trường

### Trên Windows:
```bat
python -m venv venv
call venv\Scripts\activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Trên Linux/Mac:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```
