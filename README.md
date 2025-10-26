# Recherce von Spacy Funktionen und Funktionsweisen
# spaCy Mini Text Project

Ziel:
Sentiment als Baseline trainieren und einfache Framing-Erkennung per Regeln integrieren.
Minimalstruktur. Schnell lauffähig.

## Projektstruktur

spacy-mini-text/
├─ requirements.txt
├─ README.md
├─ data/
│  ├─ train.jsonl
│  └─ dev.jsonl
├─ components.py
├─ train_sentiment.py
├─ run_pipeline.py
└─ inspect_spacy.py

## 1 Vorbereitungen

### 1.1 Repository klonen
git clone <URL>
cd spacy-mini-text

makefile

### 1.2 Virtuelle Umgebung erstellen
Windows:
python -m venv .venv
..venv\Scripts\activate

Linux / Mac:
python3 -m venv .venv
source .venv/bin/activate

### 1.3 Abhaengigkeiten installieren
pip install -r requirements.txt
python -m spacy download en_core_web_sm

## 2 Daten prüfen

Die Trainingsdaten liegen in `data/train.jsonl` und `data/dev.jsonl`.  
Format für spaCy TextCat:

{"text":"I love this product.","cats":{"pos":1.0,"neg":0.0,"neu":0.0}}

Wenn eigene Daten: gleiche Struktur beibehalten.

## 3 Modell trainieren

python train_sentiment.py

Output:
- Modell wird nach `models/textcat-mini` gespeichert
- Accuracy wird auf dev-Daten ausgegeben

## 4 Pipeline ausführen

python run_pipeline.py

Dies:
- Lädt das trainierte Modell
- Fügt Framing-Komponente + Sentiment-Regel-Komponente hinzu
- Gibt TextCat-Label, Frame-Zaehler und Regel-Sentiment aus

## 5 spaCy intern inspizieren

python inspect_spacy.py

Dies zeigt:
- Welche Pipes aktiv sind
- Welche Config genutzt wird
- Modellarchitektur-Uebersicht

## 6 Wenn Terminal neu gestartet wurde

Virtuelle Umgebung erneut aktivieren:
Windows:
..venv\Scripts\activate

Linux / Mac:
source .venv/bin/activate

Danach wieder:
python run_pipeline.py

## 7 Häufige Probleme

| Problem | Lösung |
|-------|--------|
| pip Module nicht gefunden | Sicherstellen dass `.venv` aktiviert ist |
| spacy Modell fehlt | `python -m spacy download en_core_web_sm` |
| JSONL Formatfehler | Jede Zeile exakt ein JSON Objekt, keine Kommas |

## 8 Nächste Schritte (optional / weiterführend)

- Mehr Trainingsdaten sammeln
- Frame-Wortlisten erweitern
- Cross-Validation und Confusion-Matrix mit scikit-learn
- spaCy Config + `spacy train` nutzen
- Sprachmodelle für Deutsch testen

Fertig.
Kurzer Starttest:

python train_sentiment.py

python run_pipeline.py