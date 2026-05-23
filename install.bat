@echo off
setlocal

echo Installation de BKLN-TECH SOLUTIONS...
py -m venv .venv
call .venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate

echo.
echo Installation terminee.
echo Lancez run.bat puis ouvrez http://localhost:8000/
pause
