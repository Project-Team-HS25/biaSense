#Business Logic - Textanalyse

class TextAnalyzer:
    def __init__(self):
        self.filler_words = ["und", "aber", "halt", "sozusagen", "irgendwie", "quasi"]

    def extract_filler_words(self, text):
        words = text.split()
        return [word for word in words if word.lower() in self.filler_words]

    def remove_filler_words(self, text):
        words = text.split()
        return " ".join([word for word in words if word.lower() not in self.filler_words])