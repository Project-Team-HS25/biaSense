import ollama

def analyse_text_mit_llm(text, adjective_results, verb_results, custom_prompt=None):
    """
    Lokale Analyse mit Ollama
    """
    kategorisierung = """
KATEGORISIERUNG (verwende diese Einteilung):
- Score ≥66: Positiv
- Score 40-65: Neutral
- Score <40: Negativ
"""

    if custom_prompt:
        # Bei eigenem Prompt: Regel automatisch hinzufügen
        prompt = f"""{custom_prompt}

{kategorisierung}

TEXT:
{text}

GEMESSENE WERTE (zur Information):
- Adjektiv-Score (gemessen): {adjective_results.get('average_score', 'N/A')}/100
- Verb-Score (gemessen): {verb_results.get('average_score', 'N/A')}/100
- Adjektiv-Sentiment: {adjective_results.get('sentiment', 'N/A')}
- Verb-Sentiment: {verb_results.get('sentiment', 'N/A')}

Antworte auf Deutsch."""
    else:
        # Standard-Prompt
        prompt = f"""Analysiere folgenden Text auf mögliche Bias und Tonalität:

TEXT:
{text}

QUANTITATIVE ERGEBNISSE:
- Adjektiv-Score: {adjective_results.get('average_score', 'N/A')}/100
- Verb-Score: {verb_results.get('average_score', 'N/A')}/100

{kategorisierung}

Gib eine kurze Analyse (max. 200 Wörter) auf Deutsch."""

    response = ollama.chat(
        model='phi3',
        messages=[{'role': 'user', 'content': prompt}]
    )

    return response['message']['content']


def verbessere_text_mit_llm(text, custom_prompt=None):
    """
    Llokale Textverbesserung mit Ollama
    """
    if custom_prompt:
        prompt = f"""{custom_prompt}

TEXT:
{text}

Antworte auf Deutsch."""
    else:
        prompt = f"""Formuliere folgenden Text neutraler und ausgewogener, ohne die Kernaussage zu verändern:

TEXT:
{text}

Gib nur den verbesserten Text zurück, ohne zusätzliche Erklärungen."""

    response = ollama.chat(
        model='phi3',
        messages=[{'role': 'user', 'content': prompt}]
    )

    return response['message']['content']