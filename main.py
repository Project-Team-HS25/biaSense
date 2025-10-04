####main.py
from ui.user_input import UserInput
from business_logic.text_analyzer import TextAnalyzer

def main():
    # UI: Eingaben
    text = UserInput.get_text_input()
    author_first_name = UserInput.get_author_input_first_name()
    author_last_name = UserInput.get_author_input_last_name()

    # Business Logic: Verarbeitung
    analyzer = TextAnalyzer()
    found_fillers = analyzer.extract_filler_words(text)
    clean_text = analyzer.remove_filler_words(text)

    # Ergebnisse vorbereiten
    results = {
        "author": f"{author_first_name} {author_last_name}",
        "text_length": len(text),
        "filler_words": found_fillers,
        "filler_count": len(found_fillers),
        "bias_scores": None,
        "clean_text": clean_text
    }

    # UI: Ausgabe
    UserInput.display_results(results)
    print("\n--- Text without filler words ---")
    print(results["clean_text"])

if __name__ == '__main__':
    main()