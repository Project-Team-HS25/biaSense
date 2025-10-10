#Business Logic - Textanalyse

class TextAnalyzer:
    def __init__(self):
        self.stopwords = None
        try:
            import nltk
            from nltk.corpus import stopwords
            self.stopwords = set(stopwords.words('english'))

        except Exception as e:
            print(f"NLTK nicht verfügbar: {e}")
            print("Verwende manuelle Füllwörter-Liste")
            self.stopwords = set([])

    def extract_filler_words(self, text):
        words = text.split()
        return [word for word in words if word.lower().strip('.,!?;:') in self.stopwords]

    def remove_filler_words(self, text):
        words = text.split()
        cleaned_words = []
        for word in words:
            # Entferne Satzzeichen für Vergleich, aber behalte sie im Wort
            word_clean = word.lower().strip('.,!?;:')
            if word_clean not in self.stopwords:
                cleaned_words.append(word)

        return " ".join(cleaned_words)