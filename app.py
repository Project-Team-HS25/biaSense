# Streamlit UI für Text Bias Analyzer

import streamlit as st
from business_logic.text_analyzer import TextAnalyzer

# Seiten-Konfiguration
st.set_page_config(
    page_title="Text Bias Analyzer",
    page_icon="📊",
    layout="wide"
)

# Titel und Beschreibung
st.title("📊 Text Bias Analyzer")
st.markdown("---")
st.markdown("""
Analyze your text for filler words and bias. Enter your text below and discover patterns in writing style.
""")

# Sidebar für Autor-Informationen
with st.sidebar:
    st.header("👤 Author Information")
    first_name = st.text_input("First Name:", placeholder="John")
    last_name = st.text_input("Last Name:", placeholder="Doe")

    st.markdown("---")
    st.header("⚙️ Settings")
    show_clean_text = st.checkbox("Show text without filler words", value=True)

# Hauptbereich - Texteingabe
st.header("📝 Text Input")
text = st.text_area(
    "Enter the text to analyze:",
    height=200,
    placeholder="Paste or type your text here...",
    help="Enter any text you want to analyze for filler words and bias"
)

# Analyse-Button
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    analyze_button = st.button("🔍 Analyze Text", type="primary", use_container_width=True)
with col2:
    clear_button = st.button("🗑️ Clear", use_container_width=True)

# Clear-Funktionalität
if clear_button:
    st.rerun()

# Analyse durchführen
if analyze_button:
    if not text.strip():
        st.error("⚠️ Please enter some text to analyze!")
    else:
        # Analyzer initialisieren
        analyzer = TextAnalyzer()

        # Analyse durchführen
        with st.spinner("Analyzing text..."):
            found_fillers = analyzer.extract_filler_words(text)
            clean_text = analyzer.remove_filler_words(text)

        # Erfolgsmeldung
        st.success("✅ Analysis complete!")

        st.markdown("---")

        # Ergebnisse in Spalten
        st.header("📈 Results")

        # Autor-Info
        author_name = f"{first_name} {last_name}".strip()
        if author_name:
            st.subheader(f"Author: {author_name}")

        # Metriken in Spalten
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

        with metric_col1:
            st.metric(
                label="Text Length",
                value=f"{len(text)}",
                help="Total number of characters"
            )

        with metric_col2:
            word_count = len(text.split())
            st.metric(
                label="Word Count",
                value=f"{word_count}",
                help="Total number of words"
            )

        with metric_col3:
            st.metric(
                label="Filler Words",
                value=f"{len(found_fillers)}",
                help="Number of filler words found"
            )

        with metric_col4:
            if word_count > 0:
                filler_percentage = (len(found_fillers) / word_count) * 100
                st.metric(
                    label="Filler Rate",
                    value=f"{filler_percentage:.1f}%",
                    help="Percentage of filler words"
                )

        # Füllwörter anzeigen
        if found_fillers:
            st.markdown("---")
            st.subheader("🔍 Found Filler Words")
            st.write(", ".join(found_fillers))
        else:
            st.markdown("---")
            st.info("🎉 No filler words found! Great writing!")

        # Text ohne Füllwörter
        if show_clean_text:
            st.markdown("---")
            st.subheader("✨ Text Without Filler Words")

            # Vergleich Original vs. Clean
            tab1, tab2 = st.tabs(["Original Text", "Cleaned Text"])

            with tab1:
                st.text_area("Original:", value=text, height=200, disabled=True)

            with tab2:
                st.text_area("Cleaned:", value=clean_text, height=200, disabled=True)

                # Statistik zur Verbesserung
                words_removed = len(text.split()) - len(clean_text.split())
                if words_removed > 0:
                    st.success(f"✂️ Removed {words_removed} filler words!")

        # Bias Scores (Placeholder für später)
        st.markdown("---")
        st.subheader("🎯 Bias Scores")
        st.info("💡 Bias scoring feature coming soon! This will analyze political and gender bias in the text.")

        bias_col1, bias_col2 = st.columns(2)
        with bias_col1:
            st.metric("Politics Bias", "0.0", help="Coming soon: -1 (left) to +1 (right)")
        with bias_col2:
            st.metric("Gender Bias", "0.0", help="Coming soon: -1 (female) to +1 (male)")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Text Bias Analyzer v1.0 | Built with Streamlit</p>
</div>
""", unsafe_allow_html=True)