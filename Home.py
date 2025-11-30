import streamlit as st
from PIL import Image

# 1. Konfiguration der Seite
st.set_page_config(
    page_title="BiaSense Home",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="collapsed" # Sidebar eingeklappt für cleaneren Look
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
        max-width: 1200px;
    }
    
    h1, h2, h3, p {
        text-align: center;
    }
    
    /* Buttons in den Kacheln auf volle Breite */
    .stButton button {
        width: 100%;
        background-color: white;
        color: black;
        border: 1px solid black;
    }
    .stButton button:hover {
        background-color: black;
        color: white;
        border: 1px solid black;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header Bereich mit Logo
try:
    # Logo laden und zentriert anzeigen
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("Logo-Design für biaSense2.png", use_container_width=True)
except:
    st.title("biaSense") # Fallback, falls Bild nicht gefunden wird

st.markdown("<h3 style='margin-bottom: 50px; color: #666;'>Bias Detection & Analysis Platform</h3>", unsafe_allow_html=True)

# 4. Die drei Kacheln (Grid Layout)
col1, col2, col3 = st.columns(3, gap="medium")

# --- Kachel 1: Analyzer ---
with col1:
    with st.container():
        st.subheader("Text Analyzer")
        st.write("Analysiere Texte auf potenzielle Biases, Sentiment und Framing.")
        st.write("") # Abstand
        if st.button("Start Analysis", key="btn_analyzer"):
            st.switch_page("pages/1_Analyzer.py")

# --- Kachel 2: Attention Demo ---
with col2:
    with st.container():
        st.subheader("Attention Demo")
        st.write("Visualisiere, worauf das KI-Modell im Text besonders achtet.")
        st.write("") # Abstand
        if st.button("View Demo", key="btn_attention"):
            st.switch_page("pages/2_Attention_Demo.py")

# --- Kachel 3: Rule Learner / POC ---
with col3:
    with st.container():
        st.subheader("Rule Learner")
        st.write("Trainiere und verbessere die Regeln für die Bias-Erkennung.")
        st.write("") # Abstand
        if st.button("Open Learner", key="btn_rules"):
            # Stelle sicher, dass du die Datei in pages/3_Rule_Learner.py umbenannt hast
            st.switch_page("pages/3_Rule_Learner.py") 

# 5. Footer / Zusatzinfo
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #888; font-size: 0.8em;'>
        Developed by Project Team HS25 | biaSense v1.0
    </div>
    """, 
    unsafe_allow_html=True
)
