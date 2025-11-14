# claude_analyzer.py
import ollama

def analyse_text_mit_llm(text, adjective_results, verb_results, custom_prompt=None):
    """
    Kostenlose lokale Analyse mit Ollama
    """
    # Standard-Prompt, falls kein custom_prompt angegeben
    if custom_prompt:
        # Benutzer-Prompt mit Text und Ergebnissen kombinieren
        prompt = f"""{custom_prompt}

TEXT:
{text}

QUANTITATIVE ERGEBNISSE:
- Adjektiv-Score: {adjective_results.get('average_score', 'N/A')}/100
- Verb-Score: {verb_results.get('average_score', 'N/A')}/100
- Adjektiv-Sentiment: {adjective_results.get('sentiment', 'N/A')}
- Verb-Sentiment: {verb_results.get('sentiment', 'N/A')}"""
    else:
        # Standard-Prompt
        prompt = f"""Analysiere folgenden Text auf mögliche Bias und Tonalität:

TEXT:
{text}

QUANTITATIVE ERGEBNISSE:
- Adjektiv-Score: {adjective_results.get('average_score', 'N/A')}/100
- Verb-Score: {verb_results.get('average_score', 'N/A')}/100

Gib eine kurze Analyse (max. 200 Wörter) auf Deutsch."""

    response = ollama.chat(
        model='phi3',
        messages=[{'role': 'user', 'content': prompt}]
    )

    return response['message']['content']


def verbessere_text_mit_llm(text, custom_prompt=None):
    """
    Kostenlose lokale Textverbesserung mit Ollama
    """
    if custom_prompt:
        prompt = f"""{custom_prompt}

TEXT:
{text}"""
    else:
        prompt = f"""Formuliere folgenden Text neutraler und ausgewogener: {text}"""

    response = ollama.chat(
        model='phi3',
        messages=[{'role': 'user', 'content': prompt}]
    )

    return response['message']['content']