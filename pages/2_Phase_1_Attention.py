import sys
import os

# --- PFAD-FIX START ---
# Fügt das Hauptverzeichnis (ein Level über 'pages') zum Python-Pfad hinzu
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir)
sys.path.insert(0, root_dir)
# --- PFAD-FIX ENDE ---

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from business_logic.attention_model import AttentionDemo

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

# Streamlit-Styling verstecken
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
    page_title="Self-Attention Demo - Pronomen-Resolution",
    page_icon="🔍",
    layout="wide"
)

# Header
col1, col2 = st.columns([1, 8])
with col1:
    st.image("Logo-Design für biaSense2.png", width=100)
with col2:
    st.title("Self-Attention Demo: Pronomen-Resolution")

# Einführung
st.markdown("""
Diese Demo zeigt den grundlegenden Self-Attention-Mechanismus, wie er in Transformer-Modellen verwendet wird.
Das Modell lernt, Pronomen mit ihren Bezugswörtern zu verknüpfen.""")

st.markdown("---")

st.markdown("""
**Hinweis**: Dies ist ein didaktisches Beispiel mit vortrainierten Sätzen, kein produktionsfähiges System.
""")

# Sidebar
with st.sidebar:
    st.header("Trainingsparameter")
    epochs = st.slider("Epochen", 100, 2000, 800, 100)
    learning_rate = st.slider("Lernrate", 0.01, 0.1, 0.05, 0.01)

# Modell initialisieren und trainieren
if 'model' not in st.session_state or st.sidebar.button("Neu trainieren"):
    with st.spinner("Modell wird trainiert..."):
        model = AttentionDemo()
        losses = model.train(epochs=epochs, lr=learning_rate)
        st.session_state.model = model
        st.session_state.losses = losses
    st.success(f"Training abgeschlossen nach {epochs} Epochen")

with st.sidebar:
    st.markdown("---")
    st.header("Über das Modell")
    st.markdown("""
    **Architektur:**
    - Embedding-Dimension: 32
    - Query/Key-Dimension: 32
    - Causal Masking: Aktiviert

    **Trainingsdaten:**
    - 3 Beispielsätze
    - Supervised Learning
    """)


model = st.session_state.model

# Trainingsverlauf
st.header("Trainingsverlauf")
if 'losses' in st.session_state:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        y=st.session_state.losses,
        mode='lines',
        name='Loss',
        line=dict(color='#FF6B6B', width=2)
    ))
    fig.update_layout(
        title="Loss über Epochen",
        xaxis_title="Epoche",
        yaxis_title="Loss",
        hovermode='x',
        height=300
    )
    st.plotly_chart(fig, width='stretch')

st.markdown("---")

# Analyse der Sätze
st.header("Pronomen-Attention Analyse")

# Tabs für die drei Sätze
tab1, tab2, tab3 = st.tabs([
    f"Satz 1: {model.sentences[0][:30]}...",
    f"Satz 2: {model.sentences[1][:30]}...",
    f"Satz 3: {model.sentences[2][:50]}..."
])


def display_sentence_analysis(sentence_idx, tab):
    with tab:
        # Satz anzeigen
        st.markdown(f"**Vollständiger Satz:**")
        st.info(model.sentences[sentence_idx])

        # Analyse durchführen
        analysis = model.analyze_pronoun(sentence_idx)

        # Pronomen und Ziel hervorheben
        col1, col2 = st.columns(2)
        with col1:
            st.metric(
                "Pronomen",
                f"{analysis['pronoun']} (Position {analysis['pronoun_idx']})"
            )
        with col2:
            st.metric(
                "Ziel-Substantiv",
                f"{analysis['target']} (Position {analysis['target_idx']})"
            )

        st.markdown("---")

        # Attention-Gewichte als Heatmap
        st.subheader("Attention-Gewichte Visualisierung")

        A = model.get_attention_weights(sentence_idx)
        tokens = analysis['tokens']

        # Heatmap erstellen
        fig = go.Figure(data=go.Heatmap(
            z=A,
            x=tokens,
            y=tokens,
            colorscale='RdYlGn',
            text=np.round(A, 3),
            texttemplate='%{text}',
            textfont={"size": 10},
            hoverongaps=False
        ))

        fig.update_layout(
            title=f"Attention Matrix für Satz {sentence_idx + 1}",
            xaxis_title="Attention auf Token",
            yaxis_title="Von Token",
            height=500
        )

        st.plotly_chart(fig, width='stretch')

        st.markdown("---")

        # Top-5 Attention-Ziele
        st.subheader(f"Top 5 Attention-Ziele für '{analysis['pronoun']}'")

        for i, target in enumerate(analysis['top_targets']):
            col1, col2, col3 = st.columns([2, 2, 6])

            with col1:
                st.write(f"**Rang {i + 1}**")

            with col2:
                weight_percent = target['weight'] * 100
                st.write(f"{weight_percent:.1f}%")

            with col3:
                if target['is_target']:
                    st.success(f"✓ **{target['word']}** (Position {target['index']}) - Korrektes Ziel")
                else:
                    st.write(f"{target['word']} (Position {target['index']})")

        st.markdown("---")

        # Interpretation
        st.subheader("Interpretation")

        correct_weight = analysis['attention_weights'][analysis['target_idx']] * 100

        if correct_weight > 50:
            interpretation = f"Das Modell hat gelernt, dass '{analysis['pronoun']}' hauptsächlich auf '{analysis['target']}' achten sollte ({correct_weight:.1f}% Attention-Gewicht)."
            st.success(interpretation)
        elif correct_weight > 20:
            interpretation = f"Das Modell zeigt moderate Attention von '{analysis['pronoun']}' auf '{analysis['target']}' ({correct_weight:.1f}%). Mehr Training könnte die Genauigkeit verbessern."
            st.warning(interpretation)
        else:
            interpretation = f"Das Modell hat noch nicht stark gelernt, '{analysis['pronoun']}' mit '{analysis['target']}' zu verknüpfen ({correct_weight:.1f}%). Längeres Training empfohlen."
            st.error(interpretation)


# Tabs mit Analyse füllen
display_sentence_analysis(0, tab1)
display_sentence_analysis(1, tab2)
display_sentence_analysis(2, tab3)

st.markdown("---")

# Technische Details
with st.expander("Technische Details & Einschränkungen"):
    st.markdown("""
    ### Wie funktioniert Self-Attention?

    1. **Query & Key Projektion**: Jedes Wort wird in Query- und Key-Vektoren transformiert
    2. **Attention Scores**: Berechnung der Ähnlichkeit zwischen Queries und Keys
    3. **Causal Masking**: Verhindert Zugriff auf zukünftige Tokens
    4. **Softmax**: Normalisierung zu Wahrscheinlichkeitsverteilung

    ### Trainierte Paare
    - "She" → "Anna"
    - "He" → "John"
    - "it" → "animal"

    ### Einschränkungen
    - Funktioniert nur auf den drei Trainingsbeispielen
    - Keine Generalisierung auf neue Sätze
    - Vereinfachte Architektur ohne Value-Projektionen
    - Keine Multi-Head-Attention
    - Kein Feedforward-Netzwerk
    - Rein didaktisches Beispiel

    ### Formel
    ```
    Attention(Q,K) = softmax(Q·K^T / √d_k)
    ```

    Dabei ist d_k die Dimension der Key-Vektoren (hier: 32).
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: gray;'>
    <p>Educational Purpose Only</p>
</div>
""", unsafe_allow_html=True)