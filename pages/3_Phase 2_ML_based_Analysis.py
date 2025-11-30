from locale import normalize
from operator import ne
from turtle import pos
import charset_normalizer
import pip
import streamlit as st
import spacy
from spacy.tokens import DocBin
from spacy.training import Example
from spacy.util import minibatch
import random
import numpy as np
import json
import pandas as pd
from pathlib import Path
from typing import Dict, List
from sklearn.metrics import f1_score, classification_report, accuracy_score
import sys
import os

# ------------------------------------------------------------------------------
# SYSTEM-KONFIGURATION
# ------------------------------------------------------------------------------
# Wir fügen das Hauptverzeichnis zum Pfad hinzu, damit components.py gefunden wird
sys.path.append(str(Path(__file__).parent.parent))

try:
    from components import create_framing_component, create_sentiment_rule
except ImportError:
    # Fallback, falls Komponenten nicht geladen werden können (verhindert Absturz)
    pass

# Custom CSS für das Button-Design
st.markdown("""
    <style>
    /* Buttons in den Kacheln auf volle Breite */
    .stButton button {
        width: 100%;
        background-color: white;
        color: black;
        border: 1px solid black;
        margin-top: 5px;
    }
    .stButton button:hover {
        background-color: gray;
        color: white;
        border: 1px solid black;
    }
    </style>
""", unsafe_allow_html=True)

# Streamlit-Styling für einen professionellen Look ohne Ablenkung
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stStatusWidget"] {display:none;}
    
    [data-testid="stSidebar"] {
        min-width: 300px;
        max-width: 300px;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

st.set_page_config(
    page_title="Pipeline Manager & Training",
    page_icon=None, # Keine Emojis im Tab-Titel
    layout="wide"
)

# ------------------------------------------------------------------------------
# HEADER
# ------------------------------------------------------------------------------
col1, col2 = st.columns([1, 8])
with col1:
    if os.path.exists("Logo-Design für biaSense.png"):
        st.image("Logo-Design für biaSense2.png", width=100)
    else:
        st.write("biaSense")
with col2:
    st.title("Machine Learning based Analysis")

st.markdown("""
Hier können die NLP-Modelle trainiert und die gesamte Pipeline getestet werden.
Diese Seite dient auch dazu, die zugrundeliegenden Prozesse der Sprachverarbeitung mit NLP zu verstehen.
""")

# Tabs für die verschiedenen Funktionen
tab_run, tab_train_sent, tab_train_frames = st.tabs(["Pipeline Ausführen", "Sentiment Model trainieren", "Framing Model trainieren"])

# -----------------------------------------------------------------------------
# TAB 1: PIPELINE RUNNER & ERKLÄRUNG
# -----------------------------------------------------------------------------
with tab_run:
    st.header("Pipeline Testen & Verstehen")
    
    # TEIL A: INPUT
    # -------------------------------------------------------------------------
    st.markdown("### Text Eingabe")
    default_text = "I love this product! It works great and makes me happy."
    user_text = st.text_area("Englischen Text zur Analyse eingeben:", value=default_text, height=300)

    sent_model_path = Path("models/textcat-mini")
    frames_model_path = Path("models/frames-mini")
    models_exist = sent_model_path.exists() and frames_model_path.exists()


    if not models_exist:
            st.warning("Es wurden keine trainierten Modelle gefunden. Bitte trainieren Sie zuerst die Modelle in den anderen Reitern.")

    pipeline_button = st.button("Pipeline starten")
    st.markdown("---")
    
    # TEIL B: VISUALISIERUNG & ERKLÄRUNG (2 Spalten)
    # -------------------------------------------------------------------------
    col_vis, col_expl = st.columns([1, 4], gap="small")
    
    with col_vis:
        st.markdown("### Der Prozess")
        # Platzhalter für das Bild
        st.image("Pipeline.png", width=180, use_container_width=False)

        

    with col_expl:
        st.markdown("### Was passiert im Hintergrund?")
        st.markdown("""
        Wenn Sie auf 'Starten' klicken, durchläuft der Text folgende Schritte:
                    
        ###### 
    

        ##### 1. **Tokenizer:** Der Satz wird in einzelne Wörter (Tokens) zerlegt. Aus "It's" wird "It" und "'s".
                    

        ##### 2. **Tagger & Parser:** Die Grammatik wird analysiert. Das Modell erkennt Verben, Substantive und deren Beziehung zueinander.
                    

        ##### 3. **Stopwords:** Unwichtige Füllwörter (wie "the", "is", "at") werden markiert, damit sich das Modell auf den Inhalt konzentriert.
                    

        ##### 4. **TextCat (Text Categorizer):** Hier greifen die trainierten Modelle. Sie weisen dem gesamten Text Wahrscheinlichkeiten für bestimmte Kategorien (Positiv/Negativ oder Frames) zu.
                    

        ##### 5. **Custom Components:** Ganz am Ende laufen die eigenen Regeln (z.B. Sentiment Component), um Ergebnisse zu zeigen, dass auch eigene Komponenten funktionieren würden.
        """)
        
    st.markdown("---")
    
    # TEIL C: AUSFÜHRUNG
    # -------------------------------------------------------------------------

    st.markdown("### Resultate der Analyse")
    if not pipeline_button:
        st.markdown("Auf 'Pipeline starten' klicken, um die Analyse zu sehen.")

    if pipeline_button:
        with st.spinner("Pipeline läuft... Tokenisierung... Analyse..."):
            try:
                # Modelle laden
                nlp_sent = spacy.load("models/textcat-mini")
                nlp_frames = spacy.load("models/frames-mini")

                # Custom Components anhängen
                if "framing_component" not in nlp_sent.pipe_names:
                    # Hinweis: Hier müsste die echte Komponente importiert werden, falls registriert
                    pass 
                
                # Analyse
                d_sent = nlp_sent(user_text)
                d_frames = nlp_frames(user_text)

                # Ergebnisse extrahieren
                sent_pred = max(d_sent.cats, key=d_sent.cats.get)
                sent_score = d_sent.cats[sent_pred]
                frames_pred = {k: float(v) for k, v in d_frames.cats.items() if v >= 0.5}

                # Darstellung
                st.subheader("Analyse Ergebnisse")
                r1, r2 = st.columns(2)
                
                with r1:
                    st.markdown("**Sentiment Analyse**")
                    
                    match sent_pred.lower():
                        case 'pos':
                            st.success(f"Klasse: {sent_pred.upper()} ({sent_score:.2%}), ")
                        case 'neg':
                            st.error(f"Klasse: {sent_pred.upper()} ({sent_score:.2%}), ")
                        case 'neu':
                            st.warning(f"Klasse: {sent_pred.upper()} ({sent_score:.2%}), ")
                    
                    with st.expander("Details anzeigen"):
                        st.json(d_sent.cats)

                with r2:
                    st.markdown("**Frame Analyse**")
                    if frames_pred:
                        for frame, score in frames_pred.items():
                            st.success(f"Frame: {frame} ({score:.2%})")
                    else:
                        st.write("Keine dominanten Frames gefunden.")
                    with st.expander("Details anzeigen"):
                        st.json(d_frames.cats)

            except Exception as e:
                st.error(f"Fehler beim Ausführen: {e}")

# -----------------------------------------------------------------------------
# TAB 2: SENTIMENT TRAINING
# -----------------------------------------------------------------------------
with tab_train_sent:
    st.header("Sentiment Modell Training")
    
    # ERKLÄRUNG
    with st.expander("Wie funktioniert das Training? (Hier klicken für Details)", expanded=False):
        st.markdown("""
        ### 1. Das TextCat Modell
        Das Modell verlässt sich nicht auf eine einzige Technik, sondern kombiniert zwei Ansätze:
                    
        Der "Bag-of-Words" Teil (Linear Model): Das ist der simple Teil. Er lernt stumpf Gewichtungen für einzelne Wörter.

        * *Beispiel:* Das Wort "terrible" bekommt -5 Punkte, "fantastic" bekommt +5 Punkte.

        * *Vorteil:* Extrem schnell und lernt sehr gut *spezifische Signalwörter*.

        Der "Neuronale" Teil *(CNN - Convolutional Neural Network)*: Das ist der intelligente Teil. Ein CNN schaut sich nicht nur einzelne Wörter an, sondern Wortfenster (z.B. 3-4 Wörter am Stück).
        
        * *Beispiel:* Es versteht, dass "not good" etwas anderes bedeutet als nur "good". Es *erkennt Muster in der Reihenfolge und im Kontext*.

        * *Vorteil:* Versteht Grammatik, Verneinungen und Kontext.

        ### 2. Was ist der "Loss"?
        Der Loss ist der **Fehler-Score**. Er misst den Abstand zwischen der *Vorhersage* des Modells und der *Wahrheit*.
        * *Beispiel:* Das Modell sagt "70% Positiv", aber der Text ist eigentlich "Negativ" (0%).
        * *Differenz:* Gross = **Hoher Loss**.
        * *Ziel:* Wir wollen den Loss so nah wie möglich an **0.0** bringen.
        
        ### 3. Was passiert in einem Trainings-Zyklus (Epoche)?
        Eine Epoche bedeutet, dass das Modell alle Trainingsdaten einmal gesehen hat.
        1.  **Shuffle:** Daten mischen, damit das Modell nicht die Reihenfolge auswendig lernt.
        2.  **Mini-Batch:** Wir nehmen eine kleine Gruppe Texte (z.B. 8 Stück).
        3.  **Prediction (Vorhersage):** Das Modell rät für diese 8 Texte.
        4.  **Loss Berechnung:** Wir vergleichen das Raten mit der Lösung.
        5.  **Backpropagation (Lernen):** Das ist der wichtigste Schritt! Man rechnnet zurück: *"Welches Gewicht war schuld am Fehler?"* und gewichten es ein winziges Stück weniger oder mehr (Gradient Descent).
        """)

    epochs_sent = st.number_input("Anzahl Epochen (Durchläufe)", min_value=1, max_value=50, value=10, key="epochs_sent")
    
    if st.button("Training starten (Sentiment)", key="btn_train_sent"):
        
        # UI Elemente für Live-Updates
        chart_placeholder = st.empty()
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        # Datenspeicher für Diagramm
        metrics_history = {"epoch": [], "loss": [], "accuracy": []}

        # Hilfsfunktionen
        def read_jsonl(path):
            for line in Path(path).read_text(encoding="utf-8").splitlines():
                yield json.loads(line)

        def make_docbin(nlp, path):
            db = DocBin()
            for ex in read_jsonl(path):
                doc = nlp.make_doc(ex["text"])
                doc.cats = ex["cats"]
                db.add(doc)
            return db

        def evaluate_model(nlp, docs):
            correct = 0
            total = 0
            for d in docs:
                pred = nlp(d.text)
                p = max(pred.cats, key=pred.cats.get)
                g = max(d.cats, key=d.cats.get)
                correct += int(p == g)
                total += 1
            return correct / max(total, 1)

        try:
            with st.spinner("Daten werden gelernt..."):
                # Setup
                base = spacy.load("en_core_web_sm")
                nlp = spacy.blank("en")
                nlp.tokenizer = base.tokenizer

                if "textcat" not in nlp.pipe_names:
                    textcat = nlp.add_pipe("textcat")
                    textcat.add_label("pos")
                    textcat.add_label("neg")
                    textcat.add_label("neu")

                # Daten laden
                if not os.path.exists("data/sentiment_train.jsonl"):
                    st.error("Trainingsdaten fehlen!")
                    st.stop()
                
                train_db = make_docbin(nlp, "data/sentiment_train.jsonl")
                dev_db = make_docbin(nlp, "data/sentiment_dev.jsonl")
                train_docs = list(train_db.get_docs(nlp.vocab))
                dev_docs = list(dev_db.get_docs(nlp.vocab))

                optimizer = nlp.initialize(get_examples=lambda: (Example.from_dict(d, {"cats": d.cats}) for d in train_docs))

                # Trainings-Loop
                for epoch in range(epochs_sent):
                    random.shuffle(train_docs)
                    losses = {}
                    
                    # Batch Training
                    for batch in minibatch(train_docs, size=8):
                        examples = [Example.from_dict(d, {"cats": d.cats}) for d in batch]
                        nlp.update(examples, sgd=optimizer, losses=losses)

                    # Metriken berechnen
                    current_loss = losses.get('textcat', 0)
                    current_acc = evaluate_model(nlp, dev_docs)
                    
                    # Historie updaten
                    metrics_history["epoch"].append(epoch + 1)
                    metrics_history["loss"].append(current_loss)
                    metrics_history["accuracy"].append(current_acc)
                    
                    # Live-Diagramm zeichnen (Loss normalisiert)
                    df_metrics = pd.DataFrame(metrics_history).set_index("epoch")
                    df_metrics['loss'] = df_metrics['loss'] / max(df_metrics['loss'].max(), 1)
                    chart_placeholder.line_chart(df_metrics)
                    
                    
                    status_text.text(f"Epoche {epoch+1}/{epochs_sent} | Loss: {current_loss:.4f} | Accuracy: {current_acc:.2%}")
                    progress_bar.progress((epoch + 1) / epochs_sent)

                # Speichern
                output_dir = Path("models/textcat-mini")
                output_dir.mkdir(parents=True, exist_ok=True)
                nlp.to_disk(output_dir)
                st.success(f"Training abgeschlossen! Modell gespeichert in: {output_dir}")

        except Exception as e:
            st.error(f"Fehler: {e}")

# -----------------------------------------------------------------------------
# TAB 3: FRAMES TRAINING
# -----------------------------------------------------------------------------
with tab_train_frames:
    st.header("Frames Modell Training (Multi-Label)")

    # ERKLÄRUNG
    with st.expander("Unterschied: Single-Label vs. Multi-Label", expanded=False):
        st.markdown("""
        **Das Problem:**
        Ein Text ist nicht immer nur "Positiv" ODER "Negativ". Ein Satz kann gleichzeitig "Wirtschaftlich" und "Politisch" geframed sein.
        
        **Die Lösung (Multi-Label):**
        Im Gegensatz zum Sentiment-Training (wo sich Kategorien ausschließen), darf das Modell hier für **jedes Label** einzeln entscheiden. Wir nutzen dafür eine `sigmoid` Aktivierungsfunktion statt `softmax`.
        
        **Evaluation (F1-Score):**
        Da "Accuracy" (Treffergenauigkeit) bei vielen Nullen (Labels, die NICHT zutreffen) irreführend sein kann, nutzen wir den **F1-Score**. Er balanciert Precision (Genauigkeit) und Recall (Vollständigkeit).
        """)

    epochs_frames = st.number_input("Anzahl Epochen", min_value=1, max_value=50, value=12, key="epochs_frames")

    if st.button("Training starten (Frames)", key="btn_train_frames"):
        
        chart_placeholder_f = st.empty()
        progress_bar_f = st.progress(0)
        status_text_f = st.empty()
        
        # Wir tracken hier Loss und den Macro-F1 Score
        metrics_history_f = {"epoch": [], "loss": [], "f1_macro": []}

        # Hilfsfunktionen für Frames
        def read_jsonl_f(path):
            lines = Path(path).read_text(encoding="utf-8").splitlines()
            return [json.loads(li) for li in lines]

        def collect_labels(examples):
            labels = set()
            for ex in examples:
                for k in ex["cats"].keys():
                    labels.add(k)
            return sorted(labels)
        
        def to_y(examples, labels):
            y = []
            for ex in examples:
                y.append([int(round(ex["cats"].get(lbl, 0.0))) for lbl in labels])
            return np.array(y, dtype=int)

        def predict_multilabel(nlp, examples, labels, threshold=0.5):
            y_pred = []
            for ex in examples:
                doc = nlp(ex["text"])
                row = []
                for lbl in labels:
                    p = float(doc.cats.get(lbl, 0.0))
                    row.append(1 if p >= threshold else 0)
                y_pred.append(row)
            return np.array(y_pred, dtype=int)

        try:
            with st.spinner("Training läuft..."):
                base = spacy.load("en_core_web_sm")
                nlp = spacy.blank("en")
                nlp.tokenizer = base.tokenizer

                if not os.path.exists("data/frames_train.jsonl"):
                    st.error("Daten fehlen!")
                    st.stop()

                train_raw = read_jsonl_f("data/frames_train.jsonl")
                dev_raw = read_jsonl_f("data/frames_dev.jsonl")
                labels = collect_labels(train_raw)

                if "framecat" not in nlp.pipe_names:
                    textcat = nlp.add_pipe("textcat_multilabel", name="framecat")
                    for lbl in labels:
                        textcat.add_label(lbl)

                train_examples = [Example.from_dict(nlp.make_doc(ex["text"]), {"cats": ex["cats"]}) for ex in train_raw]
                
                optimizer = nlp.initialize(get_examples=lambda: train_examples)

                for epoch in range(epochs_frames):
                    losses = {}
                    # Update (hier vereinfacht ohne Minibatch-Loop für Übersichtlichkeit, aber intern optimiert Spacy)
                    nlp.update(train_examples, sgd=optimizer, losses=losses)
                    
                    # Metriken berechnen
                    loss_val = losses.get('framecat', 0)
                    
                    # Schnelle Evaluation auf Dev-Set für Diagramm
                    y_true = to_y(dev_raw, labels)
                    y_pred = predict_multilabel(nlp, dev_raw, labels)
                    f1 = f1_score(y_true, y_pred, average='macro')

                    # Historie
                    metrics_history_f["epoch"].append(epoch + 1)
                    metrics_history_f["loss"].append(loss_val)
                    metrics_history_f["f1_macro"].append(f1)

                    # Update Chart (Loss normalisiert)
                    df_f = pd.DataFrame(metrics_history_f).set_index("epoch")
                    df_f['loss'] = df_f['loss'] / max(df_f['loss'].max(), 1)
                    chart_placeholder_f.line_chart(df_f)
                    
                    status_text_f.text(f"Epoche {epoch+1}/{epochs_frames} | Loss: {loss_val:.4f} | F1-Macro: {f1:.4f}")
                    progress_bar_f.progress((epoch + 1) / epochs_frames)

                # Speichern
                out_dir = Path("models/frames-mini")
                out_dir.mkdir(parents=True, exist_ok=True)
                nlp.to_disk(out_dir)
                st.success(f"Training fertig! Gespeichert in {out_dir}")
                
                # Abschlussbericht
                st.markdown("**Detaillierter Abschlussbericht:**")
                report_dict = classification_report(y_true, y_pred, target_names=labels, zero_division=0, output_dict=True)
                report_df = pd.DataFrame(report_dict).transpose()
                st.dataframe(report_df, use_container_width=True)

        except Exception as e:
            st.error(f"Fehler: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Educational Purpose Only</p>
</div>
""", unsafe_allow_html=True)