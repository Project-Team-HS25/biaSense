# ==============================================================================
# MODUL: Phase 3 - LLM Analyzer (UI)
# DATEI: pages/6_🤖_Phase3_LLM.py
# PROJEKT: biaSense
# ==============================================================================

from turtle import back
import streamlit as st
import sys
import os
from pathlib import Path
import subprocess
import platform
import requests # Falls noch nicht installiert: pip install requests

# ------------------------------------------------------------------------------
# PFAD-KONFIGURATION (Verbindung zum Backend)
# ------------------------------------------------------------------------------
# Fügt das Hauptverzeichnis zum Suchpfad hinzu, damit llm_analyzer.py gefunden wird
sys.path.append(str(Path(__file__).parent.parent))

try:
    # Wir importieren nur die benötigten Funktionen aus deiner Datei
    from llm_analyzer import analyse_text_mit_llm, verbessere_text_mit_llm
except ImportError as e:
    st.error(f"Import-Fehler: {e}. Bitte stelle sicher, dass 'llm_analyzer.py' im Hauptordner liegt.")
    st.stop()

# ------------------------------------------------------------------------------
# UI KONFIGURATION
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="LLM Analyzer",
    page_icon="🤖",
    layout="wide"
)

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

# Custom CSS um Standard-Elemente auszublenden
st.markdown("""
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stStatusWidget"] {display:none;}
    [data-testid="stSidebar"] { min-width: 300px; max-width: 300px; }
</style>
""", unsafe_allow_html=True)

# ------------------------------------------------------------------------------
# SESSION STATE
# ------------------------------------------------------------------------------
if 'analysis_done' not in st.session_state:
    st.session_state.analysis_done = False
if 'text' not in st.session_state:
    st.session_state.text = ""
if 'llm_result' not in st.session_state:
    st.session_state.llm_result = ""

# ------------------------------------------------------------------------------
# HEADER 
# ------------------------------------------------------------------------------
col1, col2 = st.columns([1, 8])
with col1:
    if os.path.exists("Logo-Design für biaSense2.png"):
        st.image("Logo-Design für biaSense2.png", width=100)
    else:
        st.write("BiaSense")
with col2:
    st.title("Text Analyzer")

st.markdown("---")

st.markdown(" ")

# ------------------------------------------------------------------------------
# SIDEBAR MIT AUTO-REFRESH STATUS
# ------------------------------------------------------------------------------
with st.sidebar:
    # --------------------------------------------------------------------------
    # OLLAMA STATUS FRAGMENT (Aktualisiert sich selbst)
    # --------------------------------------------------------------------------
    # run_every=1 bedeutet: Führe diese Funktion alle 1 Sekunden erneut aus
    @st.fragment(run_every=1)
    def show_ollama_status_widget():
        st.subheader("Ollama Status")
        
        # 1. Prüfen (mit kurzem Timeout, damit die UI nicht hängt)
        is_running = False
        try:
            # Timeout sehr kurz halten (0.2s), da wir jede Sekunde prüfen
            response = requests.get("http://localhost:11434", timeout=0.2)
            if response.status_code == 200:
                is_running = True
        except:
            is_running = False

        # 2. Anzeige & Button Logik
        if is_running:
            st.success("Ollama läuft! 🟢")
            # Kein Start-Button nötig, wenn es schon läuft
        else:
            st.error("Ollama ist aus 🔴")
            
            # Button zum Starten
            if st.button("Ollama starten", key="btn_start_ollama"):
                system = platform.system()
                try:
                    if system == "Darwin":  # MacOS
                        subprocess.Popen(["open", "-a", "Ollama"])
                        st.toast("Startbefehl an MacOS gesendet...", icon="⏳")
                    
                    elif system == "Windows":
                        subprocess.Popen("ollama serve", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
                        st.toast("Startbefehl an Windows gesendet...", icon="⏳")
                    
                    else:
                        st.warning("Bitte Ollama manuell im Terminal starten.")
                        
                except Exception as e:
                    st.error(f"Fehler: {e}")

    # Hier rufen wir die Fragment-Funktion auf, damit sie gerendert wird
    show_ollama_status_widget()

    st.markdown("---")
    
    # Der Reset Button (Außerhalb des Fragments, da er die ganze App betrifft)
    if st.button("Neue Analyse starten", width='stretch'):
        st.session_state.analysis_done = False
        st.session_state.text = ""
        st.session_state.llm_result = ""
        st.rerun()

# ------------------------------------------------------------------------------
# HAUPTBEREICH: EINGABE
# ------------------------------------------------------------------------------
st.header("Texteingabe:")
st.markdown("Bevor du den Text analysierst, stelle sicher, dass Ollama läuft (siehe Sidebar).")

# Textfeld ist immer sichtbar und editierbar
text_input = st.text_area(
    "Gib deinen englischen Text für die Analyse ein:",
    value=st.session_state.text,
    height=200,
    placeholder="Füge deinen Text hier ein...",
    key="input_area"
)

# Der Analyse-Button
if st.button("Analysiere den Text"):
    if not text_input.strip():
        st.error("Bitte gib zuerst einen Text ein.")
    else:
        with st.spinner("KI analysiert den Text..."):
            try:
                # Aufruf deiner Backend-Funktion
                # Wir übergeben None für adjective/verb results, da diese im Prompt optional sind
                result = analyse_text_mit_llm(
                    text=text_input, 
                    _adjective_results=None, 
                    _verb_results=None
                )
                
                # Ergebnis speichern
                st.session_state.text = text_input
                st.session_state.llm_result = result
                st.session_state.analysis_done = True
                st.rerun()
                
            except Exception as e:
                st.error(f"Fehler bei der Analyse: {e}")

# ------------------------------------------------------------------------------
# ERGEBNIS & VERBESSERUNG (Erscheint nach Klick)
# ------------------------------------------------------------------------------
if st.session_state.analysis_done:
    st.markdown("---")
    st.header("Resultate")
    
    # 1. Das Analyse-Ergebnis anzeigen
    st.subheader("Analyse-Ergebnis:")
    with st.container(border=True):
        st.markdown(st.session_state.llm_result)
    
    st.markdown("---")
    
    # 2. Verbesserungs-Bereich (Erscheint jetzt automatisch darunter)
    st.subheader("Verbesserungsvorschlag")
    
    c1, c2 = st.columns([1, 3])
    with c1:
        st.markdown("**Anpassungswunsch:**")
    
    # Prompt Feld für Verbesserung
    custom_improvement_prompt = st.text_area(
        "Was soll verbessert werden?",
        placeholder="Z.B.: Formuliere neutraler und ausgewogener...",
        height=100,
        key="improvement_prompt"
    )
    
    if st.button("Verbesserung generieren"):
        with st.spinner("KI generiert Vorschlag..."):
            try:
                # Aufruf deiner Backend-Funktion
                improved_text = verbessere_text_mit_llm(
                    text=st.session_state.text,
                    custom_prompt=custom_improvement_prompt if custom_improvement_prompt.strip() else None
                )
                
                st.text_area(
                    "Neutralere Version des Textes:",
                    value=improved_text,
                    height=300
                )
            except Exception as e:
                st.error(f"Fehler bei der Generierung: {e}")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Educational Purpose Only</p>
</div>
""", unsafe_allow_html=True)