import streamlit as st
from business_logic.text_analyzer import TextAnalyzer

hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stStatusWidget"] {display:none;}
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)


# Seiten-Konfiguration
st.set_page_config(
    page_title="Text Bias Analyzer",
    page_icon="📊",
    layout="wide"
)

# Titel und Beschreibung
col1, col2 = st.columns([1, 8])
with col1:
    st.image("Logo-Design für biaSense.png", width=100)
with col2:
    st.title("Text Bias Analyzer")
st.markdown("---")
st.markdown("""
Analysiere deinen Text auf Füllwörter und Sentiment basierend auf Adjektiven. Achtung nur englischsprachige Texte können berücksichtigt werden.
""")

# Sidebar für Einstellungen
with st.sidebar:
    st.header("Einstellungen")
    show_adjectives = st.checkbox("Zeige die Sentiment-Analyse (Adjektiv-basiert)", value=True)

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
    height=200,
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

        # Erfolgsmeldung
        st.success("Analyse komplett.")

        st.markdown("---")

        # Ergebnisse
        st.header("Resultate")

        # Autor-Info
        author_name = f"{first_name} {last_name}".strip()
        if author_name:
            st.subheader(f"Autor:in: {author_name}")

        # Adjektiv-Analyse
        if show_adjectives and adjective_results['count'] > 0:
            st.markdown("---")
            st.subheader("Sentiment-Analyse (Adjektiv-basiert)")

            # Sentiment Metriken
            sent_col1, sent_col2, sent_col3 = st.columns(3)

            with sent_col1:
                st.metric(
                    label="Gefundene Adjektive",
                    value=adjective_results['count'],
                    help="Anzahl analysierter Adjektive"
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
            for idx, (adj, score) in enumerate(sorted_adjectives):
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

                    st.write(f"{color} **{adj}**: {score}")

        elif show_adjectives:
            st.markdown("---")
            st.info("Es wurden keine Adjektive im Text gefunden.")


# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Text Bias Analyzer v1.0 | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)