#Eine Pipeline ist  eine Abfolge von Verarbeitungsschritten, die auf Textdaten angewendet werden, um sie zu analysieren und zu transformieren. 
import spacy
from components import create_framing_component, create_sentiment_rule

def main():
    # 1. Trainiertes Modell laden
    nlp = spacy.load("models/textcat-mini")

    # 2. Custom Components anhängen
    # "last=True" hängt sie ans Ende, damit zuerst Klassifikation laeuft, dann die eigenen Regeln
    nlp.add_pipe("framing_component", name="framing", last=True)
    nlp.add_pipe("sentiment_rule", name="sent_rule", last=True)

    # 3. Beispieldaten
    texts = [
        "The market will grow despite the clash",
        "I love the build quality but the cost is high",
        "This was a waste and I hate it"
    ]

    # 4. Durch die Pipeline schicken
    for t in texts:
        doc = nlp(t)
        pred = max(doc.cats, key=doc.cats.get)
        print("text:", t)
        print("textcat:", doc.cats, "pred:", pred)
        print("frames:", doc._.frames, "sentiment_rule:", doc._.sentiment_rule)
        print()

if __name__ == "__main__":
    main()
