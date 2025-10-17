# 🧠 biaSense – Data Setup & Pipeline Guide

Dieses Dokument erklärt, wie die Datenstruktur des Projekts aufgebaut ist  
und wie du die komplette Pipeline (Preprocessing → Feature Extraction → Scoring) startest.

---

## 📂 Verzeichnisstruktur

data/
│
├── raw/ # Rohdaten (deine Test- oder Trainings-Texte, .txt)
│
├── metadata/ # Informationen über die Texte
│ └── dataset_index.json # Index mit allen Pfaden, IDs und Labels
│
├── lexicons/ # Wortlisten für Feature-Extraktion (manuell gepflegt)
│ ├── economy_en.txt
│ ├── security_en.txt
│ ├── moral_en.txt
│ ├── conflict_en.txt
│ ├── victim_taeter_en.txt
│ ├── hedges_en.txt
│ ├── loaded_en.txt
│ └── blame_verbs_en.txt
│
├── processed/ # ← leer lassen (wird automatisch erstellt)
│
├── processed_features/ # ← leer lassen (wird automatisch erstellt)
│
└── scored/ # ← leer lassen (wird automatisch erstellt)

---

## 🧱 1. Vorbereitung

### a) Stelle sicher, dass dein virtuelles Environment aktiv ist:
```powershell
.\.venv\Scripts\Activate.ps1
b) Prüfe, ob spaCy funktioniert:
python -m spacy info

Wenn das Model fehlt:
python -m spacy download en_core_web_sm


🚀 2. Pipeline starten
Schritt 1: Preprocessing
Erstellt strukturierte JSONs mit Tokens, POS, Entitäten usw.

powershell
Copy code
python .\scripts\run_preprocessing.py
→ Ergebnisse erscheinen automatisch in data/processed/

Schritt 2: Feature Extraction
Berechnet Lexikon-Dichten, Hedge Scores usw.

powershell
Copy code
python .\scripts\run_features.py
→ Ergebnisse erscheinen in data/processed_features/

Schritt 3: Heuristik-Scoring
Berechnet einfache Frame-Scores (0–1) für jeden Text.

powershell
Copy code
python .\scripts\run_scoring.py
→ Ergebnisse erscheinen in data/scored/

✅ Ergebnis
Nach allen Schritten sollten folgende Ordner gefüllt sein:

perl
Copy code
data/
├── processed/              → enthält *.json mit linguistischen Daten
├── processed_features/     → enthält *.features.json mit berechneten Werten
└── scored/                 → enthält *.scores.json mit Frame-Scores