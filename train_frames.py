import json
from pathlib import Path
from typing import Dict, List # import List and Dict for type hints, welche helfen, den Code verständlicher zu machen durch Angabe der erwarteten Datentypen.

import spacy
from spacy.tokens import DocBin
from spacy.training import Example
from sklearn.metrics import f1_score, classification_report

def read_jsonl(path: str) -> List[Dict]: #diese Funktion liest eine JSONL-Datei (durch angegeben Pfad) ein und gibt eine Liste von Dictionaries zurück.
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    return [json.loads(li) for li in lines]

def collect_labels(examples: List[Dict]) -> List[str]: #extrahiert alle eindeutigen Labels aus den "cats"-Feldern der Beispiele und gibt sie als sortierte Liste zurück.
    labels = set()
    for ex in examples:
        for k in ex["cats"].keys():
            labels.add(k)
    return sorted(labels)

def make_docbin(nlp, examples: List[Dict]) -> DocBin: #erstellt ein DocBin-Objekt aus den gegebenen Beispielen, wobei jedes Beispiel in ein Doc-Objekt umgewandelt und mit den entsprechenden Kategorien versehen wird.
    db = DocBin()
    for ex in examples:
        doc = nlp.make_doc(ex["text"])
        # Multi-Label: cats ist dict label->float(zwischen 0 und 1)
        doc.cats = ex["cats"]
        db.add(doc)
    return db

def to_y(examples: List[Dict], labels: List[str]): #wandelt die "cats"-Daten der Beispiele in eine binäre Matrix um, wobei jede Zeile einem Beispiel und jede Spalte einem Label entspricht. Die Werte werden auf 0 oder 1 gerundet.
    import numpy as np
    y = []
    for ex in examples:
        y.append([int(round(ex["cats"].get(lbl, 0.0))) for lbl in labels])
    return np.array(y, dtype=int)

def predict_multilabel(nlp, examples: List[Dict], labels: List[str], threshold: float = 0.5): # macht Vorhersagen für die gegebenen Beispiele mit dem spaCy-Modell und wandelt die Vorhersagewahrscheinlichkeiten in binäre um, basierend auf der angegebenen Schwelle (threshold).
    import numpy as np
    y_pred = [] # Liste für Vorhersagen
    for ex in examples:
        doc = nlp(ex["text"]) # Verarbeitet den Text mit dem spaCy-Modell
        row = [] # Liste für die Label-Vorhersagen eines Beispiels
        for lbl in labels:
            p = float(doc.cats.get(lbl, 0.0)) # Holt die Vorhersagewahrscheinlichkeit von dem Modell für das Label
            row.append(1 if p >= threshold else 0)
        y_pred.append(row)
    return np.array(y_pred, dtype=int) # Gibt die Vorhersagen als numpy-Array zurück (format: Zeilen=Beispiele, Spalten=Labels (one-hot encoded))

def main():
    # Basis-Tokenizer nutzen
    base = spacy.load("en_core_web_sm") # ladt das vortrainierte englische spaCy-Modell
    nlp = spacy.blank("en") # erstellt eine leere spaCy-Pipeline für englische Texte
    nlp.tokenizer = base.tokenizer # übernimmt den Tokenizer aus dem vortrainierten Modell

    # Daten laden
    train_examples_raw = read_jsonl("data/frames_train.jsonl") 
    dev_examples_raw   = read_jsonl("data/frames_dev.jsonl")

    # Labels sammeln und Komponente anlegen
    labels = collect_labels(train_examples_raw)
    textcat = nlp.add_pipe("textcat_multilabel", name="framecat")
    for lbl in labels:
        textcat.add_label(lbl)

    # Example-Objekte erstellen
    # Wir wandeln jedes Beispiel in ein spaCy Example-Objekt um, da spaCy diese für das Training und Initialize erwartet.
    train_examples = [Example.from_dict(nlp.make_doc(ex["text"]), {"cats": ex["cats"]}) for ex in train_examples_raw]
    dev_examples   = [Example.from_dict(nlp.make_doc(ex["text"]), {"cats": ex["cats"]}) for ex in dev_examples_raw]

    # Initialize mit korrektem Typ (Liste von Example)
    optimizer = nlp.initialize(get_examples=lambda: train_examples)

    # Training-Loop
    for epoch in range(12):
        losses = {}
        nlp.update(train_examples, sgd=optimizer, losses=losses)
        print(f"epoch {epoch:02d} loss {losses.get('framecat', 0):.4f}")

    # Speichern
    out_dir = Path("models/frames-mini")
    out_dir.mkdir(parents=True, exist_ok=True)
    nlp.to_disk(out_dir.as_posix())
    print(f"saved to {out_dir}")

    # Evaluation (F1 micro/macro)
    # y_true aus dev
    y_true = to_y(dev_examples_raw, labels)
    # y_pred mit 0.5-Schwelle
    y_pred = predict_multilabel(nlp, dev_examples_raw, labels, threshold=0.5)

    print("\n=== Multi-Label Evaluation (threshold=0.5) ===")
    print("micro-F1:", f1_score(y_true, y_pred, average="micro"))
    print("macro-F1:", f1_score(y_true, y_pred, average="macro"))
    print("\nPer-label report:")
    print(classification_report(y_true, y_pred, target_names=labels, zero_division=0))

if __name__ == "__main__":
    main()
