@echo off
echo === Setting up biaSense Environment ===

REM Schritt 1: Virtuelle Umgebung erstellen
py -m venv .venv

REM Schritt 2: Pip aktualisieren
.\.venv\Scripts\python -m pip install --upgrade pip

REM Schritt 3: Requirements installieren
.\.venv\Scripts\python -m pip install -r requirements.txt

REM Schritt 4: Spacy Sprachmodell herunterladen
.\.venv\Scripts\python -m spacy download en_core_web_sm

echo.
echo === Setup complete! ===
echo Run the project with:
echo    .\.venv\Scripts\python quick_check.py
pause
