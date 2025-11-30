import streamlit as st
import spacy
import nltk
from nltk.corpus import movie_reviews
# export_graphviz für die grafische Darstellung
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.tree import DecisionTreeClassifier, export_text, export_graphviz
import sys
import os
import subprocess
import re  # Wichtig für die Anpassung des Graphviz-Codes
from pathlib import Path

# ------------------------------------------------------------------------------
# SYSTEM-KONFIGURATION & PFADE
# ------------------------------------------------------------------------------
# 1. Hauptverzeichnis zum Pfad hinzufügen
ROOT_DIR = Path(__file__).parent.parent
sys.path.append(str(ROOT_DIR))

# 2. NLTK Datenpfad hinzufügen (OS-Unabhängig)
# Wir suchen im Ordner "nltk_data" im Hauptverzeichnis
nltk_data_path = ROOT_DIR / "nltk_data"
# WICHTIG: Wir fügen den Pfad AM ANFANG ein (insert 0), damit er bevorzugt wird
if nltk_data_path.exists():
    nltk.data.path.insert(0, str(nltk_data_path))

st.set_page_config(page_title="Rule Learner", page_icon="📏", layout="wide")

# ------------------------------------------------------------------------------
# INITIALISIERUNG (SpaCy)
# ------------------------------------------------------------------------------
@st.cache_resource
def load_spacy_model():
    """Lädt das englische SpaCy-Modell für die Satzzerlegung."""
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        st.error("SpaCy Modell 'en_core_web_sm' nicht gefunden. Bitte installieren.")
        return None

nlp = load_spacy_model()

# ------------------------------------------------------------------------------
# HILFSFUNKTION: DOWNLOADER AUSFÜHREN
# ------------------------------------------------------------------------------
def run_downloader_script():
    """Führt das externe Download-Skript aus und fängt den Output ab."""
    script_path = ROOT_DIR / "download_nltk_movie_reviews.py"
    
    if not script_path.exists():
        st.error(f"Skript nicht gefunden: {script_path}")
        return
    
    try:
        # Skript als Subprozess starten
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True,
            text=True,
            check=False,
            encoding='utf-8', # Erzwinge UTF-8 Decodierung
            errors='replace'  # Ersetze Zeichen, die nicht decodiert werden können
        )
        
        # Output anzeigen
        if result.returncode == 0:
            st.success("Download erfolgreich! Bitte Seite neu laden.")
            # Cache leeren, damit load_data neu ausgeführt wird
            st.cache_resource.clear()
            st.rerun()
        else:
            st.error("Fehler beim Download.")
            st.code(result.stdout + "\n" + result.stderr)
            
    except Exception as e:
        st.error(f"Kritischer Fehler beim Ausführen: {e}")

# ------------------------------------------------------------------------------
# LOGIK: DATEN PRÜFEN & LADEN
# ------------------------------------------------------------------------------

def check_data_availability():
    """
    Prüft schnell (ohne Cache), ob die NLTK Daten verfügbar sind.
    Gibt True/False zurück.
    """
    try:
        # Versuch, auf die Kategorien zuzugreifen
        movie_reviews.categories()
        return True
    except (LookupError, OSError):
        return False

@st.cache_resource
def load_data_cached():
    """
    Lädt die Rohdaten aus dem NLTK Corpus.
    Wird nur ausgeführt, wenn check_data_availability True ist.
    Gecached für Performance.
    """
    try:
        texts = []
        labels = []
        for category in movie_reviews.categories():
            for fileid in movie_reviews.fileids(category):
                texts.append(movie_reviews.raw(fileid))
                labels.append(category)
        return texts, labels
    except Exception as e:
        return None, None

def train_decision_tree(texts, labels, max_depth, min_samples_leaf, max_features):
    """
    Trainiert Vectorizer und Decision Tree mit den gegebenen Parametern.
    """
    # 1. Vektorisierung (TF-IDF)
    vectorizer = TfidfVectorizer(
        max_features=max_features,
        ngram_range=(1, 2), # Einzelwörter und Bigramme
        stop_words='english' # Optional: Stopwords entfernen für cleanere Regeln
    )
    X = vectorizer.fit_transform(texts)

    # 2. Decision Tree
    clf = DecisionTreeClassifier(
        max_depth=max_depth,
        min_samples_leaf=min_samples_leaf,
        random_state=42
    )
    clf.fit(X, labels)

    return clf, vectorizer

# ------------------------------------------------------------------------------
# LOGIK: HELPER & VISUALISIERUNG
# ------------------------------------------------------------------------------
def label_to_color(label: str) -> str:
    """Ordnet Sentiment-Label eine HTML-Farbe zu."""
    if label == "pos":
        return "#28a745" # Grün
    elif label == "neg":
        return "#dc3545" # Rot
    return "#6c757d" # Grau

def analyze_text_html(text, clf, vectorizer):
    """Klassifiziert Sätze und gibt HTML zurück."""
    doc = nlp(text)
    html_parts = []
    
    for sent in doc.sents:
        # Vektorisieren
        sent_vec = vectorizer.transform([sent.text])
        # Vorhersagen
        pred_label = clf.predict(sent_vec)[0]
        # Färben
        color = label_to_color(pred_label)
        # HTML bauen (mit Tooltip für Debugging optional denkbar)
        html_parts.append(f'<span style="background-color: {color}20; border-bottom: 2px solid {color}; padding: 2px; border-radius: 3px;" title="{pred_label}">{sent.text}</span>')
    
    return " ".join(html_parts)

# ------------------------------------------------------------------------------
# UI AUFBAU
# ------------------------------------------------------------------------------
col1, col2 = st.columns([1, 8])
with col1:
    if os.path.exists("Logo-Design für biaSense.png"):
        st.image("Logo-Design für biaSense2.png", width=100)
    else:
        st.write("biaSense")
with col2:
    st.title("Rule Learner (Decision Tree)")

st.markdown("""
Hier trainieren wir einen **Explainable AI (XAI)** Ansatz. Ein Entscheidungsbaum lernt
feste Regeln (z.B. *wenn "terrible" vorkommt -> Negativ*), die wir visualisieren können.
""")

# SESSION STATE FÜR MODELL
if 'dt_model' not in st.session_state:
    st.session_state.dt_model = None
if 'dt_vectorizer' not in st.session_state:
    st.session_state.dt_vectorizer = None

# --- BEREICH 0: SETUP (DATEN PRÜFUNG) ---
# Wir nutzen die ungecachte Check-Funktion, um den aktuellen Status zu prüfen
data_is_ready = check_data_availability()

if not data_is_ready:
    st.warning("Die Trainingsdaten (Movie Reviews) fehlen noch.")
    with st.expander("Setup & Daten (Hier klicken)", expanded=True):
        st.info("Klicke auf den Button, um den NLTK-Datensatz einmalig herunterzuladen.")
        if st.button("NLTK Daten herunterladen (Einmalig ausführen)", type="primary"):
            with st.spinner("Lade Daten..."):
                run_downloader_script()
else:
    # Daten sind da -> Lade sie in den Cache (falls noch nicht passiert)
    texts, labels = load_data_cached()


# --- BEREICH 1: TRAINING ---
with st.expander("⚙️ Training & Parameter", expanded=True):
    # Sperren, wenn keine Daten da sind
    disable_training = not data_is_ready
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Hyperparameter")
        p_max_depth = st.slider("Max Depth (Tiefe des Baums)", 2, 20, 5, help="Je tiefer, desto komplexer (Gefahr von Overfitting).", disabled=disable_training)
        p_min_samples = st.slider("Min Samples Leaf", 1, 100, 10, help="Mindestanzahl an Beispielen pro Regel (Blatt).", disabled=disable_training)
        p_max_features = st.select_slider("Max Features (Vokabular)", options=[500, 1000, 2000, 5000], value=2000, disabled=disable_training)

    with col2:
        st.subheader("Training Steuerung")
        st.write("Datensatz: NLTK Movie Reviews (2000 Texte)")
        
        if st.button("Modell trainieren", disabled=disable_training):
            # Wir holen die Daten sicher aus dem Cache
            texts_train, labels_train = load_data_cached()
            
            if texts_train:
                with st.spinner("Extrahiere Features & Trainiere Baum..."):
                    clf, vec = train_decision_tree(texts_train, labels_train, p_max_depth, p_min_samples, p_max_features)
                    
                    # Im State speichern
                    st.session_state.dt_model = clf
                    st.session_state.dt_vectorizer = vec
                    st.success("Training abgeschlossen!")
            else:
                st.error("Konnte Daten nicht laden, obwohl sie vorhanden sein sollten. Bitte Cache leeren.")
            
    # Ergebnisse anzeigen (Grafischer Baum & Text-Regeln)
    if st.session_state.dt_model:
        st.markdown("---")
        st.subheader("Visualisierung des gelernten Baums")
        
        # Feature Namen holen
        feature_names = st.session_state.dt_vectorizer.get_feature_names_out().tolist()
        
        # Tab-Auswahl für verschiedene Ansichten
        viz_tab1, viz_tab2 = st.tabs(["Grafik (Graphviz)", "Text (Regeln)"])
        
        with viz_tab1:
            try:
                # 1. Exportiere den Baum in das DOT-Format (Rohdaten)
                dot_data = export_graphviz(
                    st.session_state.dt_model,
                    out_file=None,
                    feature_names=feature_names,
                    class_names=st.session_state.dt_model.classes_,
                    filled=True,
                    rounded=True,
                    special_characters=True,
                    impurity=False # Versteckt den Gini-Index
                )
                
                # ------------------------------------------------------------------
                # AGGRESSIVE POST-PROCESSING (Pfeile, Farben, Values)
                # ------------------------------------------------------------------
                
                # A. Values entfernen (Robustes Regex)
                # Entfernt alles von 'value' oder '\nvalue' bis zum schließenden ']'
                # (?s) macht den Punkt auch über Zeilenumbrüche hinweg matchbar, falls nötig
                dot_data = re.sub(r'(\\n)?value = \[.*?\]', '', dot_data)
                
                # B. True/False durch Y/N ersetzen (Regex für Toleranz bei Leerzeichen)
                # headlabel="True" -> Y (Grün)
                dot_data = re.sub(r'headlabel\s*=\s*"True"', 'headlabel="Y", labelfontcolor="#28a745"', dot_data)
                # headlabel="False" -> N (Rot)
                dot_data = re.sub(r'headlabel\s*=\s*"False"', 'headlabel="N", labelfontcolor="#dc3545"', dot_data)
                
                # C. Knoten-Farben anpassen (Zeile für Zeile Iteration)
                lines = dot_data.split('\n')
                new_lines = []
                for line in lines:
                    # Wir prüfen, ob es eine Knoten-Definition ist (kein Pfeil) und ein Label hat
                    if '->' not in line and '[label=' in line:
                        if 'class = pos' in line:
                            # Positiv -> Grün (#d4edda) - Ersetze vorhandenen fillcolor
                            line = re.sub(r'fillcolor="[^"]+"', 'fillcolor="#d4edda"', line)
                        elif 'class = neg' in line:
                            # Negativ -> Rot (#f8d7da) - Ersetze vorhandenen fillcolor
                            line = re.sub(r'fillcolor="[^"]+"', 'fillcolor="#f8d7da"', line)
                            
                    new_lines.append(line)
                
                dot_data = "\n".join(new_lines)
                
                # Zeige den bearbeiteten Graph an
                st.graphviz_chart(dot_data)
                
                st.caption("Legende: Pfeil nach Links = Ja, Pfeil nach Rechts = Nein. **Grün** = positives Review, **Rot** = negatives Review.")
                
            except Exception as e:
                st.error(f"Fehler bei der Visualisierung: {e}")
                st.caption("Fallback auf Text-Ansicht empfohlen.")

        with viz_tab2:
            # Klassische Text-Regeln als Fallback
            rules_text = export_text(st.session_state.dt_model, feature_names=feature_names, max_depth=20)
            st.code(rules_text, language="text")

# --- BEREICH 2: TESTING ---
st.markdown("---")
st.header("Test Bereich")

if st.session_state.dt_model is None:
    st.info("Bitte trainiere zuerst das Modell oben.")
else:
    test_text = st.text_area(
        "Text zum Testen (Englisch):",
        value="The new policy decision was announced yesterday. Experts say the outcome could be bad for the economy. Some commentators, however, are cautiously optimistic.",
        height=150
    )
    
    if st.button("Analysieren"):
        if test_text:
            st.subheader("Ergebnis (Satz-basiert)")
            # Analyse aufrufen
            html_result = analyze_text_html(test_text, st.session_state.dt_model, st.session_state.dt_vectorizer)
            
            # Legende
            st.markdown("""
            <span style="color:#28a745; font-weight:bold;">GRÜN = Positiv</span> | 
            <span style="color:#dc3545; font-weight:bold;">ROT = Negativ</span>
            """, unsafe_allow_html=True)
            
            # Ergebnis rendern
            st.markdown(f'<div style="line-height: 1.8; font-size: 1.1em; background-color: #f0f2f6; padding: 20px; border-radius: 10px; color: black;">{html_result}</div>', unsafe_allow_html=True)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Educational Purpose Only</p>
</div>
""", unsafe_allow_html=True)






