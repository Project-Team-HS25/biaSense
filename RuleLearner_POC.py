import nltk
from nltk.corpus import movie_reviews

import spacy  # Wird für die Satzzerlegung verwendet

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier, export_text


# ----------------------------------------------------
# 1. TRAINING & INITIALISIERUNG (einmalig beim App-Start)
# ----------------------------------------------------
# In einem UI (Webapp, Desktop-App, etc.) möchtest du das Modell
# nur EINMAL beim Start der Anwendung trainieren – nicht bei jeder Anfrage.
#
# Diese Funktion lädt die Trainingsdaten, erzeugt die TF-IDF-Features
# und trainiert den Entscheidungsbaum (Rule-Learner).
# Sie gibt das fertig trainierte Modell + den Vectorizer zurück.
# ----------------------------------------------------

def train_sentiment_model():
    """
    Lädt den NLTK-Filmkritik-Datensatz ("movie_reviews"),
    wandelt ihn mit TF-IDF in Feature-Vektoren um,
    trainiert einen DecisionTreeClassifier (Rule-Learner)
    und gibt (clf, vectorizer) zurück.
    """

    # Lade den Datensatz (nur beim ersten Aufruf notwendig)
    #nltk.download('movie_reviews') -> wurde im file download bereits heruntergeladen

    texts = []   # Speichert die Texte der Reviews
    labels = []  # Speichert das jeweilige Label: "pos" oder "neg"

    # movie_reviews.categories() gibt ["pos", "neg"] zurück
    for category in movie_reviews.categories():
        # movie_reviews.fileids(category) → alle Dokumente dieser Kategorie
        for fileid in movie_reviews.fileids(category):
            texts.append(movie_reviews.raw(fileid))   # kompletter Review-Text
            labels.append(category)                   # zugehöriges Label

    # ----------------------------------------------------
    # TF-IDF-Vektorisierung
    # ----------------------------------------------------
    # Der TfidfVectorizer wandelt rohe Texte in numerische Features um.
    # max_features begrenzt die Anzahl der Wörter/Wortpaare (Speicheroptimierung).
    # ngram_range=(1,2) → auch Wortpaare ("not good", "very bad") werden verwendet.
    # Der Vektorizer "lernt", welche Wörter im Training vorkamen.
    # ----------------------------------------------------
    vectorizer = TfidfVectorizer(
        max_features=2000,
        ngram_range=(1, 2)
    )

    # Berechne die TF-IDF-Matrix für alle Trainingsbeispiele
    X = vectorizer.fit_transform(texts)

    # ----------------------------------------------------
    # Entscheidungsbaum (Rule Learner)
    # ----------------------------------------------------
    # DecisionTreeClassifier erzeugt direkt "interpretable rules".
    # max_depth begrenzt Komplexität, damit Regeln lesbar bleiben.
    # min_samples_leaf verhindert Overfitting, indem jeder Blattknoten
    # mindestens 10 Beispiele enthalten muss.
    # ----------------------------------------------------
    clf = DecisionTreeClassifier(
        max_depth=5,
        min_samples_leaf=10
    )

    # Trainiere den Baum mit den TF-IDF-Features
    clf.fit(X, labels)

    # Optionale Ausgabe der gelernten Regeln für Debugging / Dokumentation
    feature_names = vectorizer.get_feature_names_out().tolist()
    rules = export_text(clf, feature_names=feature_names)

    print("=== Learned Rules ===")
    print(rules)

    # Zurückgeben des gelernten Modells
    return clf, vectorizer


# ----------------------------------------------------
# 2. spaCy INITIALISIEREN (ebenfalls einmalig beim Start)
# ----------------------------------------------------

def init_spacy():
    """
    Lädt das englische spaCy-Sprachmodell.
    Wir verwenden es ausschließlich zur Satzzerlegung (doc.sents).
    """
    return spacy.load("en_core_web_sm")


# ----------------------------------------------------
# 3. Hilfsfunktion: Label → HTML-Farbe
# ----------------------------------------------------

def label_to_color(label: str) -> str:
    """
    Ordnet jedem Sentiment-Label eine Farbe zu.
    Diese Farben werden später in HTML verwendet.
    """
    if label == "pos":
        return "green"
    elif label == "neg":
        return "red"
    else:
        return "purple"  # Für mögliche neutrale Erweiterungen


# ----------------------------------------------------
# 4. GLOBALE INITIALISIERUNG (einmal bei App-Start)
# ----------------------------------------------------
# Dadurch wird das Modell nur EINMAL trainiert.
# Wenn du ein UI baust (Flask, Streamlit, React-Frontend),
# wird dieses File importiert – und automatisch geladen.
# ----------------------------------------------------

clf, vectorizer = train_sentiment_model()
nlp = init_spacy()


# ----------------------------------------------------
# 5. ZENTRALE FUNKTION FÜR EIN UI
# ----------------------------------------------------
# analyze_text(text) → nimmt ROHEN BENUTZER-TEXT aus UI und:
# - zerlegt ihn in Sätze
# - klassifiziert jeden Satz separat
# - gibt vollständig eingefärbtes HTML zurück
#
# Diese Funktion ist 1:1 im UI aufrufbar.
# ----------------------------------------------------

def analyze_text(text: str) -> str:
    """
    Empfängt einen beliebigen Input-Text,
    klassifiziert jeden Satz mit dem trainierten Rule-Learner
    und gibt farbiges HTML zurück.
    """

    # Verarbeite den Text mit spaCy → liefert Sätze
    doc = nlp(text)
    colored_output = ""

    for sent in doc.sents:
        # Satz mit demselben TF-IDF-Vektorizer transformieren wie die Trainingsdaten
        sent_vec = vectorizer.transform([sent.text])

        # Baum liefert Label ("pos" oder "neg")
        pred_label = clf.predict(sent_vec)[0]

        # passende Farbe bestimmen
        color = label_to_color(pred_label)

        # HTML für diesen Satz generieren
        colored_output += f'<p><span style="color:{color}">{sent.text}</span></p>\n'

    return colored_output


# ----------------------------------------------------
# 6. OPTIONALER LOKALER TEST (nur beim Direktausführen)
# ----------------------------------------------------

if __name__ == "__main__":
    test_text = """
    The new policy decision was announced yesterday.
    Experts say the outcome could be terrible for the economy.
    Some commentators, however, are cautiously optimistic.
    """

    html = analyze_text(test_text)

    print("\n=== Colored Output (HTML) ===\n")
    print(html)

    # Optional: Ausgabe in HTML-Datei schreiben
    # with open("sentiment_output.html", "w", encoding="utf-8") as f:
    #     f.write(html)