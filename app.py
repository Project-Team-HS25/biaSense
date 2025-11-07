import streamlit as st
from business_logic.text_analyzer import TextAnalyzer

hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stStatusWidget"] {display:none;}
    
    /* Sidebar breiter machen */
    [data-testid="stSidebar"] {
        min-width: 300px;
        max-width: 300px;
    }

</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Seiten-Konfiguration
st.set_page_config(
    page_title="Text Bias Analyzer (Sentiment-Analyse)",
    page_icon="📊",
    layout="wide"
)

# Titel und Beschreibung
col1, col2 = st.columns([1, 8])
with col1:
    st.image("Logo-Design für biaSense.png", width=100)
with col2:
    st.title("Text Analyzer")
st.markdown("---")
st.markdown("""
Analysiere deinen Text basierend auf Adjektiven und/oder Verben. Achtung: Nur englischsprachige Texte können berücksichtigt werden.
Die Analyse verwendet Lemmatisierung, um verschiedene Wortformen zu erkennen (z.B. "running" → "run", "loved" → "love").
""")

# Sidebar für Einstellungen
with st.sidebar:
    st.header("Einstellungen")
    show_adjectives = st.checkbox("Sentiment-Analyse Adjektive", value=True)
    show_verbs = st.checkbox("Sentiment-Analyse Verben", value=True)
    show_lemmatization = st.checkbox("Zeige Lemmatisierung", value=True, help="Zeigt wie Wörter auf ihre Grundform reduziert werden")


# Autor-Informationen (oberhalb der Texteingabe)
st.header("Autor:inneninformation")
author_col1, author_col2 = st.columns(2)
with author_col1:
    first_name = st.text_input("Vorname:", placeholder="Max")
with author_col2:
    last_name = st.text_input("Nachname:", placeholder="Muster")

st.markdown("---")

# Hauptbereich - Texteingabe
st.header("Texteingabe in Englisch:")
text = st.text_area(
    "Gib deinen Text für die Analyse ein:",
    height=300,
    placeholder="Füge deinen Text hier ein oder schreibe deinen Text hier...",
    help="Enter any text you want to analyze"
)

# Analyse-Button
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    analyze_button = st.button("Analysiere den Text", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("Lösche den Text", use_container_width=True)

# Clear-Funktionalität
if clear_button:
    st.rerun()

# Analyse durchführen
if analyze_button:
    if not text.strip():
        st.error("Stop! Du musst zuerst deinen Text für die Analyse eingeben.")
    else:
        # Analyzer initialisieren
        analyzer = TextAnalyzer()

        # Analyse durchführen
        with st.spinner("Text wird analysiert..."):
            found_fillers = analyzer.extract_filler_words(text)
            clean_text = analyzer.remove_filler_words(text)
            adjective_results = analyzer.analyze_adjectives(text)
            verb_results = analyzer.analyze_verbs(text)

            # Lemmatisierung für Anzeige (optional)
            if show_lemmatization:
                lemmatized = analyzer.lemmatize_text(text)

        # Erfolgsmeldung
        st.success("Analyse abgeschlossen.")

        st.markdown("---")

        # Ergebnisse
        st.header("Resultate")

        # Autor-Info
        author_name = f"{first_name} {last_name}".strip()
        if author_name:
            st.subheader(f"Autor:in: {author_name}")


        # Lemmatisierung anzeigen (optional)
        if show_lemmatization:
            st.header("Lemmatisierung")
            st.markdown("**Wortformen, die auf ihre Grundform reduziert wurden:**")

            lemma_changes = [(orig, lemma) for orig, lemma in lemmatized
                             if orig.lower().strip('.,!?;:') != lemma]

            if lemma_changes:
                # Gruppiere und zähle die Lemmatisierungen
                lemma_counts = {}
                for original, lemma in lemma_changes:
                    key = (original.lower().strip('.,!?;:'), lemma)
                    if key in lemma_counts:
                        lemma_counts[key] += 1
                    else:
                        lemma_counts[key] = 1

                # Sortiere nach Häufigkeit (absteigend)
                sorted_lemmas = sorted(lemma_counts.items(), key=lambda x: x[1], reverse=True)

                # Zeige in Spalten
                lemma_cols = st.columns(4)
                for idx, ((original, lemma), count) in enumerate(sorted_lemmas):
                    col_idx = idx % 4
                    with lemma_cols[col_idx]:
                        if count > 1:
                            st.write(f"**{original}** ({count}x) → {lemma}")
                        else:
                            st.write(f"**{original}** → {lemma}")
            else:
                st.info("Keine Lemmatisierung nötig - alle Wörter sind bereits in Grundform.")

        # Adjektiv-Analyse
        if show_adjectives and adjective_results['count'] > 0:
            st.markdown("---")
            st.subheader("Adjektiv-Analyse")

            # Sentiment Metriken
            sent_col1, sent_col2, sent_col3 = st.columns(3)

            with sent_col1:
                st.metric(
                    label="Gefundene Adjektive",
                    value=adjective_results['count'],
                    help="Anzahl analysierter Adjektive (Lemmas)"
                )

            with sent_col2:
                score = adjective_results['average_score']
                st.metric(
                    label="Durchschnittsscore",
                    value=f"{score} / 100",
                    help="0 = sehr negativ, 100 = sehr positiv"
                )

            with sent_col3:
                sentiment = adjective_results['sentiment']
                sentiment_emoji = {
                    'positive': 'Positiv',
                    'neutral': 'Neutral',
                    'negative': 'Negativ'
                }
                st.metric(
                    label="Gesamtstimmung",
                    value=sentiment_emoji.get(sentiment, sentiment),
                    help="Basierend auf durchschnittlichem Adjektiv-Score"
                )

            # Liste der gefundenen Adjektive
            st.markdown("**Gefundene Adjektive:**")

            # Sortiere nach Score (höchste zuerst)
            sorted_adjectives = sorted(
                adjective_results['found_adjectives'],
                key=lambda x: x[1],
                reverse=True
            )

            # Zeige in Spalten
            adj_cols = st.columns(3)
            for idx, (adj, score, count, originals) in enumerate(sorted_adjectives):
                col_idx = idx % 3
                with adj_cols[col_idx]:
                    # Farbcodierung
                    if score >= 80:
                        color = "🟢"
                    elif score >= 60:
                        color = "🟡"
                    elif score >= 40:
                        color = "🟠"
                    else:
                        color = "🔴"

                    st.write(f"{color} **{adj}**: {score} ({count}x)")

        elif show_adjectives:
            st.markdown("---")
            st.info("Es wurden keine Adjektive im Text gefunden.")

 # Verb-Analyse
        if show_verbs and verb_results['count'] > 0:
            st.markdown("---")
            st.subheader("Verb-Analyse")

            # Verb Metriken
            verb_col1, verb_col2, verb_col3 = st.columns(3)

            with verb_col1:
                st.metric(
                    label="Gefundene Verben",
                    value=verb_results['count'],
                    help="Anzahl analysierter Verben (Lemmas)"
                )

            with verb_col2:
                verb_score = verb_results['average_score']
                st.metric(
                    label="Durchschnittsscore",
                    value=f"{verb_score} / 100",
                    help="0 = sehr negativ, 100 = sehr positiv"
                )

            with verb_col3:
                verb_sentiment = verb_results['sentiment']
                sentiment_emoji = {
                    'positiv': 'Positiv',
                    'neutral': 'Neutral',
                    'negativ': 'Negativ'
                }
                st.metric(
                    label="Gesamtstimmung",
                    value=sentiment_emoji.get(verb_sentiment, verb_sentiment),
                    help="Basierend auf durchschnittlichem Verb-Score"
                )

            # Liste der gefundenen Verben
            st.markdown("**Gefundene Verben:**")

            # Sortiere nach Score
            sorted_verbs = sorted(
                verb_results['found_verbs'],
                key=lambda x: x[1],
                reverse=True
            )

            # Zeige in Spalten
            verb_cols = st.columns(3)
            for idx, (verb, score, count, originals) in enumerate(sorted_verbs):
                col_idx = idx % 3
                with verb_cols[col_idx]:
                    if score >= 80:
                        color = "🟢"
                    elif score >= 60:
                        color = "🟡"
                    elif score >= 40:
                        color = "🟠"
                    else:
                        color = "🔴"

                    if count > 1:
                        st.write(f"{color} **{verb}**: {score} ({count}x)")
                    else:
                        st.write(f"{color} **{verb}**: {score}")

        elif show_verbs:
            st.markdown("---")
            st.info("Keine Verben im Text gefunden.")


    # Gesamt-Sentiment (Kombination aus Adjektiv- und Verb-Analyse)
        if (show_adjectives and adjective_results['count'] > 0) or (show_verbs and verb_results['count'] > 0):
            st.markdown("---")
            st.subheader("Gesamtstimmung (Adjektive + Verben)")

            # Durchschnitt berechnen
            scores = []
            if adjective_results['count'] > 0:
                scores.append(adjective_results['average_score'])
            if verb_results['count'] > 0:
                scores.append(verb_results['average_score'])

            if scores:
                combined_score = sum(scores) / len(scores)
                if combined_score >= 66:
                    overall_sentiment = "Positiv"
                    color = "🟢"
                elif combined_score >= 40:
                    overall_sentiment = "Neutral"
                    color = "🟡"
                else:
                    overall_sentiment = "Negativ"
                    color = "🔴"

                st.metric(
                    label="Gesamtstimmung",
                    value=f"{color} {overall_sentiment} ({combined_score:.1f} / 100)",
                    help="Durchschnitt aus Adjektiv- und Verb-Sentiment"
                )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Text Bias Analyzer v2.0 mit Lemmatisierung | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)