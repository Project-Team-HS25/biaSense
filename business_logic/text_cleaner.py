# business_logic/text_cleaner.py

class TextCleaner:
    def __init__(self):
        # einfache Stopwort-Liste (kann später erweitert oder durch externe Datei ersetzt werden)
        self.stopwords = {"and", "or", "but", "the", "a", "an", "of", "to"}

    def remove_stopwords(self, text: str) -> str:
        words = text.split()
        filtered_words = [w for w in words if w.lower() not in self.stopwords]
        return " ".join(filtered_words)