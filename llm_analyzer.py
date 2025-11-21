import ollama

SYSTEM_PROMPT = """Du bist ein Sentiment-Analyse Experte.

WICHTIG: Sentiment-Scores sind IMMER 0-100 (niemals negativ!).
- 0-20: sehr negativ
- 20-40: negativ  
- 40-60: neutral
- 60-80: positiv
- 80-100: sehr positiv

Beispiel: "terrible" = 15/100, "amazing" = 90/100"""


def analyse_text_mit_llm(text, _adjective_results=None, _verb_results=None, custom_prompt=None):

    base_instruction = """Kategorisierung: ≥66 Positiv | 40-65 Neutral | <40 Negativ

Verwende NUR Scores 0-100. Negative Wörter = niedrige Scores (z.B. 15/100).

TEXT:
{text}

{task}

Antworte auf Deutsch."""

    task = custom_prompt if custom_prompt else "Analysiere Sentiment (Adjektive, Verben, Gesamtstimmung)."

    prompt = base_instruction.format(text=text, task=task)

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