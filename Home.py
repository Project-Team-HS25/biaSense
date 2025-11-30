from narwhals import col
import streamlit as st
from PIL import Image

# 1. Konfiguration der Seite
st.set_page_config(
    page_title="BiaSense Home",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Custom CSS für das Kachel-Design und Zentrierung
st.markdown("""
    <style>
    /* Container für die Kacheln stylen */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"] {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 20px;
        transition: transform 0.2s, box-shadow 0.2s;
        border: 1px solid #E0E0E0;
        height: 100%;
    }

    /* Hover-Effekt für die Container (Kacheln) */
    div[data-testid="stVerticalBlock"] > div[data-testid="stVerticalBlock"]:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        border-color: #000000;
    }

    /* Titel und Header zentrieren */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    h1, h2, h3, p {
        text-align: center;
    }

    /* Styling für die Phasen-Header in den Kacheln */
    .phase-header {
        font-size: 1.2em;
        font-weight: bold;
        margin-bottom: 10px;
        text-align: center;
        color: #ffffff;
    }

    .phase-desc {
        font-size: 0.9em;
        color: #fafafa;
        text-align: justify;
        margin-bottom: 20px;
        min-height: 120px; /* Damit die Buttons auf gleicher Höhe bleiben */
    }
    
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

# 3. Header Bereich mit Logo
try:
    col1, col2, col3 = st.columns([2, 3, 2])
    with col2:
        st.image("Logo-Design für biaSense2.png", use_container_width=True)
except:
    st.title("biaSense")

st.markdown("<h3 style='margin-bottom: 0px; color: #fafafa;'>Bias Detection & Analysis Platform</h3>", unsafe_allow_html=True)

# 4. Die drei Spalten für die Phasen
col1, col2, col3 = st.columns(3, gap="large")

# --- Spalte 1: Phase 1 (Basismodell & Attention) ---
with col1:
    with st.container():
        st.markdown('<div class="phase-header">Phase 1 - Basismodell</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="phase-desc">
            Entwicklung eines regelbasierten Python-Modells, das Adjektive und Verben erkennt, 
            deren Polarität bewertet (inkl. Lemmatisierung) und einen Sentiment-Score berechnet. 
            Zusätzlich wird ein PoC erstellt, der zeigt, wie satz- und abschnittsübergreifender 
            Kontext (Attention) hergestellt werden kann.
            </div>
        """, unsafe_allow_html=True)

        col1_1, col1_2 = st.columns(2, gap="small")

        with col1_1:
            with st.container():
                if st.button("Basic Analyzer", key="btn_ph1_basic", use_container_width=True):
                    st.switch_page("pages/1_Phase_1_basic_Analyzer.py")

        with col1_2:
            with st.container():    
                if st.button("Attention Demo (PoC)", key="btn_ph1_attention", use_container_width=True):
                    st.switch_page("pages/2_Phase_1_Attention.py")

# --- Spalte 2: Phase 2 (ML & Rule Learner) ---
with col2:
    with st.container():
        st.markdown('<div class="phase-header">Phase 2 - ML-Modelle</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="phase-desc">
            Training eines Modells auf gelabelten Texten zur automatisierten Bias-Erkennung und 
            Vergleich mit Phase 1. Weiterführendes PoC mittels Rule-Learner und NLTK-Datenbank, 
            um Sentiment-Analysen durchzuführen und gelernte Regeln transparent zurückzugeben.
            </div>
        """, unsafe_allow_html=True)

        st.write("") # Platzhalter für Layout-Balance

        col2_1, col2_2 = st.columns(2, gap="small")

        with col2_1:
            with st.container():
                if st.button("ML Based Analysis", key="btn_ph2_ml", use_container_width=True):
                    st.switch_page("pages/3_Phase 2_ML_based_Analysis.py")
        with col2_2:
            with st.container():            
                if st.button("Rule Learner (PoC)", key="btn_ph2_rule", use_container_width=True):
                    st.switch_page("pages/4_Phase_2_Rulelearner.py")

# --- Spalte 3: Phase 3 (LLM) ---
with col3:
    with st.container():
        st.markdown('<div class="phase-header">Phase 3 - LLM Einsatz</div>', unsafe_allow_html=True)
        st.markdown("""
            <div class="phase-desc">
            Einsatz eines Large Language Models (z. B. GPT-basiert) und gezieltes Prompt Engineering. 
            Ziel ist es, vergleichbare Sentiment- oder Bias-Scores zu generieren, um den Einfluss 
            des Modells selbst auf die Analyseergebnisse zu untersuchen.
            </div>
        """, unsafe_allow_html=True)
        

        st.write("") # Platzhalter für Layout-Balance

        if st.button("LLM Analysis", key="btn_ph3_llm", use_container_width=True):
            st.switch_page("pages/5_Phase_3_LLM_Analysis.py")


# 5. Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; font-size: 0.8em;'>
        Developed by Project Team HS25 | biaSense v2.0
    </div>
    """, 
    unsafe_allow_html=True
)