#Business Logic - Textanalyse

class TextAnalyzer:
    def __init__(self):
        self.filler_words = [
            "like", "just", "really", "very", "actually", "basically", "literally",
            "seriously", "honestly", "obviously", "clearly", "definitely",
            "sort", "kind", "maybe", "perhaps", "possibly", "probably",
            "somewhat", "rather", "quite", "fairly", "pretty",
            "so", "such", "totally", "completely", "absolutely", "entirely",
            "extremely", "incredibly", "remarkably", "particularly",
            "then", "now", "well", "anyway", "meanwhile", "eventually",
            "somehow", "somewhat", "essentially", "practically", "virtually",
            "apparently", "seemingly", "supposedly", "allegedly",
            "anyway", "anyhow", "basically", "essentially", "fundamentally",
            "simply", "merely", "only", "hardly", "barely", "nearly", "and", "or", "is", "for"
            ]

    def extract_filler_words(self, text):
        words = text.split()
        return [word for word in words if word.lower().strip('.,!?;:') in self.filler_words]

    def remove_filler_words(self, text):
        words = text.split()
        cleaned_words = []
        for word in words:
            # Entferne Satzzeichen für Vergleich, aber behalte sie im Wort
            word_clean = word.lower().strip('.,!?;:')
            if word_clean not in self.filler_words:
                cleaned_words.append(word)

        return " ".join(cleaned_words)