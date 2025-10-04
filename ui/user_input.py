#Benutzereingaben

class UserInput:

    @staticmethod
    def get_text_input():
        """Fragt Benutzer nach Text"""
        print("\n--- Text Bias Analyzer ---\n")
        while True:
            text_input = input("Please enter the text to be analyzed:\n> ").strip()
            if text_input and len(text_input) < 20000:
                return text_input
            print("Error: Text cannot be empty. Please try again.")

    @staticmethod
    def get_author_input_first_name():
        """Fragt Benutzer nach Autor Vorname"""
        while True:
            first_name = input("\nPlease enter the author's first name:\n> ").strip()
            if first_name and len(first_name) < 50:
                return first_name
            print("Error: First name must be between 1-50 characters. Please try again.")

    @staticmethod
    def get_author_input_last_name():
        """Fragt Benutzer nach Autor Nachname"""
        while True:
            last_name = input("\nPlease enter the author's last name:\n> ").strip()
            if last_name and len(last_name) < 50:
                return last_name
            print("Error: Last name must be between 1-50 characters. Please try again.")

    @staticmethod
    def display_results(analysis_results):
        """Zeigt Analyseergebnisse an"""
        print("\n" + "=" * 60)
        print("Your analysis results:")
        print("=" * 60)
        print(f"Author: {analysis_results['author']}")
        print(f"Text length: {analysis_results['text_length']} characters")
        print(f"\nExtracted filler words: {analysis_results['filler_words']}")
        print(f"Filler count: {analysis_results['filler_count']}")

        if analysis_results.get('bias_scores'):
            print(f"\n--- Bias Scores ---")
            print(f"Politics Bias: {analysis_results['bias_scores']['politics']}")
            print(f"Gender Bias: {analysis_results['bias_scores']['gender']}")
        print("=" * 60 + "\n")