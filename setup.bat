@echo off
python -m venv venv
call venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm
echo Setup hoàn tất!
pause