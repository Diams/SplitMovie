@echo off

python -m venv env

call env\Scripts\activate.bat
python -m pip install -U pip
pip install -r requirements.txt

pause
