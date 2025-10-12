# biaSense
Sentiment klassifikations Projekt

***Regeln***
- Bitte nur getesteten und reviewten Code in den Mainbranch mergen (Review durch andere Person wäre gut)
- Dokumentation auf deutsch
- Kommentare auf deutsch im Code
  
🧩 Setup Instructions
1️⃣ Voraussetzungen
Python 3.11 oder höher (empfohlen: Python.org Download
)
Internetverbindung (für Paket-Installation)

2️⃣ Projekt klonen oder herunterladen
git clone https://github.com/<username>/biaSense.git
cd biaSense

(Oder ZIP herunterladen und entpacken.)

3️⃣ Installation (automatisch, ohne PowerShell-Freigabe)
🪟 Windows
Im Powershell Terminal:
cmd /c setup.cmd

eingeben oder manuell ausführen:

py -m venv .venv
.\.venv\Scripts\python -m pip install --upgrade pip
.\.venv\Scripts\python -m pip install -r requirements.txt
.\.venv\Scripts\python -m spacy download en_core_web_sm

🍎 macOS / Linux
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python -m spacy download en_core_web_sm

4️⃣ Projekt testen
Nach der Installation:
# Windows
.\.venv\Scripts\python quick_check.py
# macOS / Linux
./.venv/bin/python quick_check.py

Erwartete Ausgabe:

Samples: 3
dict_keys([...])
positive apple_vision_pro.txt

5️⃣ Troubleshooting
Problem	Lösung
pip nicht gefunden	python -m ensurepip --upgrade
spacy Modell fehlt	python -m spacy download en_core_web_sm
kein Internet / Firewall	Offline-Installation mit pip download verwenden
ExecutionPolicy Fehler	Nicht nötig – Skript nutzt direkte Python-Aufrufe