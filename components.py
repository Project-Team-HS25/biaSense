from spacy.language import Language
from spacy.tokens import Doc
#Doc ist eine Datenstruktur in spaCy für einen kompletten text mit Tokens, Annotationen etc.
#Language ist die Basisklasse für spaCy-Sprachmodelle und ermöglicht das Hinzufügen von Komponenten zur Verarbeitungspipeline (ermöglicht die Erstellung benutzerdefinierter NLP-Komponenten).

# 1. Frame-Definitionen: einfache Wortlisten je Frame (serh vereinfachte Version)
FRAMES = {
    "conflict": {"vs", "battle", "fight", "clash"},
    "economic": {"cost", "market", "jobs", "growth"},
    "human_interest": {"child", "family", "story", "heart"},
}

# 2. Sentiment-Stichwortlisten (sehr vereinfachte Version)
POS_WORDS = {"great", "good", "excellent", "love", "amazing"}
NEG_WORDS = {"bad", "terrible", "hate", "awful", "waste"}

@Language.factory("framing_component") #erstellt eine Fabrikfunktion für die Framing-Komponente
def create_framing_component(nlp, name):
    # 3. Custom-Attribut am Doc: doc._.frames wird am doc angehängt
    Doc.set_extension("frames", default=dict, force=True)

    def pipe(doc: Doc): #Die Pipe-Funktion analysiert den Text und zählt Vorkommen von Wörtern aus den definierten Frames. 
        # Es wird ein Dictionary mit den Zählungen der Frames erstellt und dem Doc-Objekt hinzugefügt. im Format doc._.frames = {'conflict': 2, 'economic': 1, 'human_interest': 0}
        counts = {k: 0 for k in FRAMES}
        for t in doc:
            lemma = t.lemma_.lower()  # Grundform eines Wortes, z. B. "grow" statt "grows"
            for k, lex in FRAMES.items(): 
                if lemma in lex:
                    counts[k] += 1
        doc._.frames = counts
        return doc

    return pipe

@Language.factory("sentiment_rule") #Diese "sentimentanalyse" wird nicht so tiefgehend sein wie spacy's eingebaute Textkategorisierung, jedoch kann so der Unterschied betrachtet werden.
def create_sentiment_rule(nlp, name):
    # 4. weiteres Custom-Attribut: doc._.sentiment_rule wird am doc angehängt
    Doc.set_extension("sentiment_rule", default=0, force=True)

    def pipe(doc: Doc): #Die Pipe-Funktion analysiert den Text und berechnet eine Sentiment-Bewertung basierend auf vordefinierten positiven und negativen Wörtern.
        score = 0
        for t in doc:
            w = t.lower_
            if w in POS_WORDS:
                score += 1
            if w in NEG_WORDS:
                score -= 1
        doc._.sentiment_rule = score
        return doc

    return pipe
