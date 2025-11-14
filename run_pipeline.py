# Eine Pipeline ist  eine Abfolge von Verarbeitungsschritten, die auf Textdaten angewendet werden, um sie zu analysieren und zu transformieren. 
import spacy
from components import create_framing_component, create_sentiment_rule

def main():
    # Trainiertes Sentiment Modell laden
    nlp_sent = spacy.load("models/textcat-mini")
    
    # Trainiertes Frames Modell laden
    nlp_frames = spacy.load("models/frames-mini")

    # Custom Components anhängen
    # "last=True" hängt sie ans Ende, damit zuerst Klassifikation läuft, dann die eigenen Regeln
    nlp_sent.add_pipe("framing_component", name="framing", last=True)
    nlp_frames.add_pipe("sentiment_rule", name="sent_rule", last=True)

    # Beispieldaten
    texts = [
        "I love this product! It works great and makes me happy.", # positive sentiment
        "This is the worst service I have ever experienced.", # negative sentiment
        "Monsters and Dead People are soooo cute! I wish i could cuddle thm all day.", # positive sentiment
        "hollywood has crafted a solid formula for successful animated movies , and ice age only improves on it , with terrific computer graphics , inventive action sequences and a droll sense of humor .", # positive sentiment
        "the film contains no good jokes , no good scenes , barely a moment when carvey 's saturday night live-honed mimicry rises above the level of embarrassment .", # negative sentiment
        "I purchased this puzzle because of the cute holiday picture. Unfortunately, the puzzle was very poorly made, the pieces were cracked and split on the top, and pieces were still locked together in the box because they hadn't been cut all the way through. Because I like to frame puzzles the damaged pieces are unacceptable. This puzzle was useless and a waste of money. 1 star.", # negative sentiment
        "Please visit http://vzerohost.com/info and sign up to alpha test a image hosting service!", # neutral sentiment
        "This is not fantastic, it is not even good" #negative sentiment
    ]

    # Durch die Pipeline schicken
    for t in texts:
        d_sent   = nlp_sent(t)
        d_frames  = nlp_frames(t)

        # Sentiment: exklusive Klassen
        sent_pred = max(d_sent.cats, key=d_sent.cats.get)

        # Vorhersage des Frames durchführen. Es sind mehrere möglich, alle p>=0.5 werden ausgegeben
        frames_pred = {k: float(v) for k, v in d_frames.cats.items() if v >= 0.5}

        print("text:", t)
        print("sentiment:", sent_pred, d_sent.cats)
        print("frames>=0.5:", frames_pred if frames_pred else "{}")
        print()

if __name__ == "__main__":
    main()
