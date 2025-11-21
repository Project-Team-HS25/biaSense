import streamlit as st
from business_logic.text_analyzer import TextAnalyzer
from llm_analyzer import analyse_text_mit_llm, verbessere_text_mit_llm

st.set_page_config(
    page_title="Text Analyzer",
    page_icon="📊",
    layout="wide"
)

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

# Session State initialisieren
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'text' not in st.session_state:
    st.session_state.text = ""
if 'adjective_results' not in st.session_state:
    st.session_state.adjective_results = {}
if 'verb_results' not in st.session_state:
    st.session_state.verb_results = {}
if 'lemmatized' not in st.session_state:
    st.session_state.lemmatized = []
if 'first_name' not in st.session_state:
    st.session_state.first_name = ""
if 'last_name' not in st.session_state:
    st.session_state.last_name = ""

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
    st.header("Phase 1 - Sentiment Analyse")
    show_adjectives = st.checkbox("Sentiment-Analyse Adjektive", value=True)
    show_verbs = st.checkbox("Sentiment-Analyse Verben", value=True)
    show_lemmatization = st.checkbox("Zeige Lemmatisierung", value=True,
                                     help="Zeigt wie Wörter auf ihre Grundform reduziert werden")

    # KI-Analyse Optionen
    st.markdown("---")
    st.header("Phase 3 - KI-Analyse")
    use_llm = st.checkbox("KI Analyse aktivieren", value=True, help="Nutzt das Modell Ollama für die Analyse.")
    show_improved_text = st.checkbox("Verbesserungsvorschlag anzeigen", value=True,
                                     help="KI schlägt neutralere Formulierung vor")

# Autor-Informationen (oberhalb der Texteingabe)
st.header("Autor:inneninformation")
author_col1, author_col2 = st.columns(2)
with author_col1:
    first_name = st.text_input("Vorname:", value=st.session_state.first_name, placeholder="Max")
with author_col2:
    last_name = st.text_input("Nachname:", value=st.session_state.last_name, placeholder="Muster")

st.markdown("---")

# Hauptbereich - Texteingabe
st.header("Texteingabe in Englisch:")
text = st.text_area(
    "Gib deinen Text für die Analyse ein:",
    value=st.session_state.text,
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
    st.session_state.analysis_done = False
    st.session_state.text = ""
    st.session_state.adjective_results = {}
    st.session_state.verb_results = {}
    st.session_state.lemmatized = []
    st.session_state.first_name = ""
    st.session_state.last_name = ""
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
            else:
                lemmatized = []

        # In Session State speichern
        st.session_state.analysis_done = True
        st.session_state.text = text
        st.session_state.adjective_results = adjective_results
        st.session_state.verb_results = verb_results
        st.session_state.lemmatized = lemmatized
        st.session_state.first_name = first_name
        st.session_state.last_name = last_name

        # Erfolgsmeldung
        st.success("Analyse abgeschlossen.")

# Ergebnisse anzeigen (wenn Analyse durchgeführt wurde)
if st.session_state.analysis_done:
    st.markdown("---")
    st.header("Resultate")

    # Autor-Info
    author_name = f"{st.session_state.first_name} {st.session_state.last_name}".strip()
    if author_name:
        st.subheader(f"Autor:in: {author_name}")

    # Lemmatisierung anzeigen (optional)
    if show_lemmatization and st.session_state.lemmatized:
        st.header("Lemmatisierung")
        st.markdown("**Wortformen, die auf ihre Grundform reduziert wurden:**")

        lemma_changes = [(orig, lemma) for orig, lemma in st.session_state.lemmatized
                         if orig.lower().strip('.,!?;:') != lemma]

        if lemma_changes:
            lemma_counts = {}
            for original, lemma in lemma_changes:
                key = (original.lower().strip('.,!?;:'), lemma)
                if key in lemma_counts:
                    lemma_counts[key] += 1
                else:
                    lemma_counts[key] = 1

            sorted_lemmas = sorted(lemma_counts.items(), key=lambda x: x[1], reverse=True)

            lemma_cols = st.columns(4)
            for idx, ((original, lemma), count) in enumerate(sorted_lemmas):
                col_idx = idx % 4
                with lemma_cols[col_idx]:
                    if count > 1:
                        st.write(f"**{original}** ({count}x) → {lemma}")
                    else:
                        st.write(f"**{original}** → {lemma}")
        else:
            st.info("Keine Lemmatisierung nötig, da alle Wörter bereits in ihrer Grundform.")

    # Adjektiv-Analyse
    if show_adjectives and st.session_state.adjective_results.get('count', 0) > 0:
        st.markdown("---")
        st.subheader("Adjektiv-Analyse")

        sent_col1, sent_col2, sent_col3 = st.columns(3)

        with sent_col1:
            st.metric(
                label="Gefundene Adjektive",
                value=st.session_state.adjective_results['count'],
                help="Anzahl analysierter Adjektive (Lemmas)"
            )

        with sent_col2:
            score = st.session_state.adjective_results['average_score']
            st.metric(
                label="Durchschnittsscore",
                value=f"{score} / 100",
                help="0 = sehr negativ, 100 = sehr positiv"
            )

        with sent_col3:
            sentiment = st.session_state.adjective_results['sentiment']
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

        st.markdown("**Gefundene Adjektive:**")

        sorted_adjectives = sorted(
            st.session_state.adjective_results['found_adjectives'],
            key=lambda x: x[1],
            reverse=True
        )

        adj_cols = st.columns(3)
        for idx, (adj, score, count, originals) in enumerate(sorted_adjectives):
            col_idx = idx % 3
            with adj_cols[col_idx]:
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
    if show_verbs and st.session_state.verb_results.get('count', 0) > 0:
        st.markdown("---")
        st.subheader("Verb-Analyse")

        verb_col1, verb_col2, verb_col3 = st.columns(3)

        with verb_col1:
            st.metric(
                label="Gefundene Verben",
                value=st.session_state.verb_results['count'],
                help="Anzahl analysierter Verben (Lemmas)"
            )

        with verb_col2:
            verb_score = st.session_state.verb_results['average_score']
            st.metric(
                label="Durchschnittsscore",
                value=f"{verb_score} / 100",
                help="0 = sehr negativ, 100 = sehr positiv"
            )

        with verb_col3:
            verb_sentiment = st.session_state.verb_results['sentiment']
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

        st.markdown("**Gefundene Verben:**")

        sorted_verbs = sorted(
            st.session_state.verb_results['found_verbs'],
            key=lambda x: x[1],
            reverse=True
        )

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

    # Gesamt-Sentiment
    if (show_adjectives and st.session_state.adjective_results.get('count', 0) > 0) or \
       (show_verbs and st.session_state.verb_results.get('count', 0) > 0):
        st.markdown("---")
        st.subheader("Gesamtstimmung (Adjektive + Verben)")

        scores = []
        if st.session_state.adjective_results.get('count', 0) > 0:
            scores.append(st.session_state.adjective_results['average_score'])
        if st.session_state.verb_results.get('count', 0) > 0:
            scores.append(st.session_state.verb_results['average_score'])

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

    # KI Analyse
    if use_llm and st.session_state.analysis_done:
        st.markdown("---")
        st.header("🤖 KI Analyse")

        st.markdown("**Definiere deine Analyse-Anforderungen:**")
        custom_analysis_prompt = st.text_area(
            "Eigener Analyse-Prompt (optional):",
            placeholder="Z.B.: Analysiere den Text auf geschlechtsspezifische Sprache und gib konkrete Beispiele...",
            help="Lass das Feld leer für Standard-Analyse oder gib deine eigenen Anforderungen ein",
            height=100,
            key="custom_analysis"
        )

        analyze_ki_button = st.button("KI-Analyse starten", type="primary", key="start_ki_analysis")

        if analyze_ki_button:
            with st.spinner("KI analysiert den Text..."):
                try:
                    llm_analysis = analyse_text_mit_llm(
                        st.session_state.text,
                        st.session_state.adjective_results,
                        st.session_state.verb_results,
                        custom_prompt=custom_analysis_prompt if custom_analysis_prompt.strip() else None
                    )
                    st.markdown("### Analyse-Ergebnis:")
                    st.markdown(llm_analysis)
                except Exception as e:
                    st.error(f"Fehler bei der KI-Analyse: {str(e)}")

    if use_llm and show_improved_text and st.session_state.analysis_done:
        st.markdown("---")
        st.subheader("📝 Verbesserungsvorschlag")

        custom_improvement_prompt = st.text_area(
            "Eigener Verbesserungs-Prompt (optional):",
            placeholder="Z.B.: Formuliere den Text um für ein jüngeres Publikum und verwende einfachere Sprache...",
            help="Lass das Feld leer für Standard-Verbesserung oder gib deine eigenen Anforderungen ein",
            height=100,
            key="custom_improvement"
        )

        improve_button = st.button("Verbesserung generieren", type="secondary", key="generate_improvement")

        if improve_button:
            with st.spinner("KI erstellt Verbesserungsvorschlag..."):
                try:
                    improved_text = verbessere_text_mit_llm(
                        st.session_state.text,
                        custom_prompt=custom_improvement_prompt if custom_improvement_prompt.strip() else None
                    )
                    st.text_area(
                        "Neutralere Version des Textes:",
                        value=improved_text,
                        height=200,
                        key="improved_output"
                    )
                except Exception as e:
                    st.error(f"Fehler beim Erstellen des Verbesserungsvorschlags: {str(e)}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Text Bias Analyzer v2.0 mit KI-Unterstützung | Built with Streamlit & Ollama</p>
</div>
""", unsafe_allow_html=True)