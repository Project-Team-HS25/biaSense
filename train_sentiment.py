import spacy
from spacy.tokens import DocBin
from pathlib import Path # Ptahlib ist eine Standardbibliothek in Python zur Arbeit mit Dateipfaden. (keine NLP-spezifische Bibliothek)

# Hilfsfunktion zum Einlesen von JSONL-Dateien
def read_jsonl(path):
    import json
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        yield json.loads(line)

# DocBin (serialisierte Sammlung von Docs) aus JSONL-Daten erstellen, lässt sich schnell in spaCy laden (gut für große Datensätze)
def make_docbin(nlp, path):
    db = DocBin()
    for ex in read_jsonl(path):
        doc = nlp.make_doc(ex["text"])   # nur tokenisieren, noch keine Analyse
        doc.cats = ex["cats"]            # Ziel-Labels an das Doc haengen cats = {'pos': 1, 'neg': 0, 'neu': 0} (wird für spacy TextCat benötigt)
        db.add(doc)
    return db

def main():
    # 1. Tokenizer aus einem bestehenden englischen Modell uebernehmen
    # hier wird der Tokenizer aus core_web_sm verwendet, da er besser ist als der einfache Blank-Tokenizer
    # Funktionalität des Tokenizers: Zerlegt Text in Tokens (Wörter, Satzzeichen etc.) es wird ebenfalls auf spezielle Fälle wie Abkürzungen, Zahlen und zusammengesetzte Wörter geachtet.
    base = spacy.load("en_core_web_sm") # en_core_web_sm ist ein vortrainiertes englisches Sprachmodell von spaCy, das grundlegende NLP-Funktionalitäten wie Tokenisierung, etc. bietet.
    nlp = spacy.blank("en") # Estellen der leeren Pipeline für englische Texte und deren Verarbeitung
    nlp.tokenizer = base.tokenizer # hier wird nur der Tokenizer von en_core_web_sm übernommen. Die restlichen Komponenten (wie POS-Tagging, NER etc.) werden nicht übernommen.

    # 2. Textklassifikator anlegen und Labels definieren
    textcat = nlp.add_pipe("textcat")
    textcat.add_label("pos")
    textcat.add_label("neg")
    textcat.add_label("neu")

    # 3. Trainings- und Dev-Daten laden
    train_db = make_docbin(nlp, "data/train.jsonl")
    dev_db = make_docbin(nlp, "data/dev.jsonl")
    train_docs = list(train_db.get_docs(nlp.vocab)) # umwandeln der komprimierten DocBin-Daten in eine Liste von Doc-Objekten
    dev_docs = list(dev_db.get_docs(nlp.vocab)) # das gleiche für die Dev-Daten

    # 4. Parameter initialisieren
    # aufsetzen des modells für das Training (Initialisierung der Gewichte, definieren der Zielvariablen "cats" : {'pos': 0, 'neg': 0, 'neu': 0} )
    optimizer = nlp.initialize(get_examples=lambda: ((d, {"cats": d.cats}) for d in train_docs))

    # 5. Einfacher Trainingsloop
    for epoch in range(10): # 10 mal die ganzen Trainingsdaten durchlaufen (10 Epochen) (aufpassen! overfitting oder underfitting möglich)
        losses = {} # Dictionary zum Speichern der Verluste / Fehler (losses) während des Trainings
        for d in train_docs:
            nlp.update([(d, {"cats": d.cats})], sgd=optimizer, losses=losses) # Modell wird mit den Trainingsdaten trainiert, die Gewichte werden angepasst und die Verluste (losses) gespeichert
        print(f"epoch {epoch} loss {losses.get('textcat', 0):.2f}") # Ausgabe des Verlusts (loss) für die Textklassifikationskomponente nach jeder Epoche (loss unter 0.5 ist gut)

    # 6. Speichern
    Path("models").mkdir(exist_ok=True) # Erstellen des Ordners "models", falls er noch nicht existiert
    nlp.to_disk("models/textcat-mini") # Speichern des trainierten Modells auf die Festplatte im Ordner "models/textcat-mini"

    # 7. Schnelle Evaluation auf Dev
    correct = 0 # Zähler für korrekte Vorhersagen
    total = 0  # Zähler für Gesamtvorhersagen
    for d in dev_docs: 
        pred = nlp(d.text) # Aufrufen des Modells für Vorhersage für den Text im Dev-Datensatz (Validierungsdatensatz)
        p = max(pred.cats, key=pred.cats.get)     # wählt die Klasse mit der höchsten Wahrscheinlichkeit als Vorhersage
        g = max(d.cats, key=d.cats.get)           # bestimmt die tatsächliche Klasse aus den Ziel-Labels (g = ground truth)
        correct += int(p == g)
        total += 1
    acc = correct / max(total, 1) # Berechnung der Genauigkeit (accuracy) des Modells auf dem Dev-Datensatz
    print(f"dev accuracy {acc:.2f}")

if __name__ == "__main__":
    main()
