Abort UI / exit Terminal with ctrl + c

# Phase 1
## Setup
install ollama from https://ollama.com/download
open CMD
write: ollama pull phi3
wait for full download.


# Phase 2

Ziel:
Sentiment als Baseline trainieren und einfache Framing-Erkennung per Regeln integrieren.
Minimalstruktur. Schnell lauffähig.


## 1 Vorbereitungen

### 1.1 Virtuelle Umgebung erstellen (da systemabhängig)
Windows:
python -m venv .venv
-> es sollte nun ein .venv Ordner im Projektverzeichnis entstanden sein
.venv\Scripts\Activate

Linux / Mac:
python3 -m venv .venv
source .venv/bin/activate

### 1.2 Abhaengigkeiten installieren
py -m pip install -r requirements.txt
py -m spacy download en_core_web_sm

## 2 Daten prüfen

Die Trainingsdaten liegen in `data/train.jsonl` und `data/dev.jsonl`.  
Format für spaCy TextCat:

{"text":"I love this product.","cats":{"pos":1.0,"neg":0.0,"neu":0.0}}

Wenn eigene Daten: gleiche Struktur beibehalten.

## 3 Modell trainieren

py train_sentiment.py
py train_frames.py

Output:
- Modell wird nach `models/xxx-mini` gespeichert
- Accuracy wird auf dev-Daten ausgegeben

## 4 Pipeline ausführen

python run_pipeline.py

Dies:
- Lädt das trainierte Modell
- Fügt Framing-Komponente + Sentiment-Regel-Komponente hinzu
- Gibt TextCat-Label, Frame-Zaehler und Regel-Sentiment aus

## 5 Wenn Terminal neu gestartet wurde

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
# biaSense
Sentiment klassifikations Projekt

***Regeln***
- Bitte nur getesteten und reviewten Code in den Mainbranch mergen (Review durch andere Person wäre gut)
- Dokumentation auf deutsch
- Kommentare auf deutsch im Code
  
https://github.com/orgs/Project-Team-HS25/projects/1

