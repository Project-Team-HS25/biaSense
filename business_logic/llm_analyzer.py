import ollama

SYSTEM_PROMPT = """Du bist ein Sentiment-Analyse Experte.
WICHTIG: Sentiment-Scores sind IMMER 0-100 (niemals negativ!).
- 0-20: sehr negativ
- 21-40: negativ  
- 41-60: neutral
- 61-80: positiv
- 81-100: sehr positiv
Beispiel: "terrible" = 15/100, "amazing" = 90/100"""

def analyse_text_mit_llm(text):
    base_instruction = """Kategorisierung: 0-20: sehr negativ, 21-40: negativ, 41-60: neutral, 61-80: positiv, 81-100: sehr positiv
Verwende NUR Scores 0-100. Negative Wörter = niedrige Scores (z.B. 15/100).
TEXT:
{text}
Analysiere Sentiment (Adjektive, Verben, Gesamtstimmung).
Antworte auf Deutsch."""
    
    prompt = base_instruction.format(text=text)
    
    response = ollama.chat(
        model='phi3',
        messages=[
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'user', 'content': prompt}
        ]
    )
    return response['message']['content']

def verbessere_text_mit_llm(text, custom_prompt=None):

    task = custom_prompt if custom_prompt else "Formuliere neutraler und ausgewogener."

    prompt = f"""{task}

TEXT:
{text}

Gib nur den verbesserten Text zurück."""

    response = ollama.chat(
        model='phi3',
        messages=[{'role': 'user', 'content': prompt}]
    )

    return response['message']['content']
