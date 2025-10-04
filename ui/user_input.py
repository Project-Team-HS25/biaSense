#Benutzereingaben

class UserInput:

    @staticmethod
    def get_text_input():
        """Fragt Benutzer nach Text"""
        print("\n--- Text Bias Analyzer ---\n")
        text_input = input("Please enter the text to be analyzed:\n> ")
        return text_input.strip()

    @staticmethod
    def get_author_input_first_name():
        """Fragt Benutzer nach Autor Vorname"""
        first_name = input("\nPlease enter the author's first name:\n> ")
        return first_name.strip()

    @staticmethod
    def get_author_input_last_name():
        """Fragt Benutzer nach Autor Nachname"""
        last_name = input("\nPlease enter the author's last name:\n> ")
        return last_name.strip()

    @staticmethod
    def display_results(analysis_results):
        """Zeigt Analyseergebnisse an"""
        print("\n" + "=" * 60)
        print("Your analysis results:")
        print("=" * 60)
        print(f"Author: {analysis_results['author']}")
        print(f"Text length: {analysis_results['text_length']} sign")
        print(f"\nExtracted filler words: {analysis_results['filler_words']}")
        print(f"Filler count: {analysis_results['filler_count']}")

        if analysis_results.get('bias_scores'):
            print(f"\n--- Bias Scores ---")
            print(f"Politics Bias: {analysis_results['bias_scores']['politics']}")
            print(f"Gender Bias: {analysis_results['bias_scores']['gender']}")
        print("=" * 60 + "\n")
