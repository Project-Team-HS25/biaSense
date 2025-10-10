#Business Logic - Textanalyse
import csv
import os

class TextAnalyzer:
    def __init__(self):
        self.stopwords = None
        self.use_spacy = False
        self.adjectives = {}
        try:
            import spacy
            nlp = spacy.load("en_core_web_sm")
            self.stopwords = nlp.Defaults.stop_words
            self.use_spacy = True

        except Exception as e:
            print(f"Spacy nicht verfügbar: {e}")
            print("Verwende manuelle Füllwörter-Liste")
            self.stopwords = {"like", "just", "really", "very", "actually", "basically", "literally",
                "seriously", "honestly", "obviously", "clearly", "definitely",
                "sort", "kind", "maybe", "perhaps", "possibly", "probably",
                "somewhat", "rather", "quite", "fairly", "pretty",
                "so", "such", "totally", "completely", "absolutely", "entirely",
                "extremely", "incredibly", "remarkably", "particularly",
                "then", "now", "well", "anyway", "meanwhile", "eventually",
                "somehow", "essentially", "practically", "virtually",
                "apparently", "seemingly", "supposedly", "allegedly",
                "anyhow", "fundamentally",
                "simply", "merely", "only", "hardly", "barely", "nearly",
                "and", "or", "is", "for", "the", "a", "an", "to", "in", "on", "at"}
        try:
            csv_path = os.path.join("business_logic", "adjectives.csv")
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    adjective = row['adjective'].strip().lower()
                    score = int(row['score'])
                    self.adjectives[adjective] = score
        except FileNotFoundError:
            print("Die Datei adjectives.csv konnte nicht gefunden werden.")
            self.adjectives = {}
        except Exception as e:
            print(f"Fehler beim Laden der Adjektive: {e}")
            self.adjectives = {}


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

    def analyze_adjectives(self, text):
        words = text.split()
        found_adjectives = []

        for word in words:
            word_clean = word.lower().strip('.,!?;:')
            if word_clean in self.adjectives:
                score = self.adjectives[word_clean]
                found_adjectives.append((word, score))

        # Durchschnitt berechnen
        if found_adjectives:
            avg_score = sum(score for _, score in found_adjectives) / len(found_adjectives)

            # Sentiment bestimmen
            if avg_score >= 60:
                sentiment = "positiv"
            elif avg_score >= 40:
                sentiment = "neutral"
            else:
                sentiment = "negativ"
        else:
            avg_score = 50  # Neutral wenn keine Adjektive gefunden
            sentiment = "neutral"

        return {
            'found_adjectives': found_adjectives,
            'average_score': round(avg_score, 1),
            'sentiment': sentiment,
            'count': len(found_adjectives)
        }

    def get_sentiment_category(self, score):
        if score >= 80:
            return "sehr positiv"
        elif score >= 60:
            return "positiv"
        elif score >= 40:
            return "neutral"
        elif score >= 20:
            return "negativ"
        else:
            return "sehr negativ"





"""class TextAnalyzer:
    def __init__(self):
        self.stopwords = None
        try:
            import nltk
            #nltk.download('stopwords')
            from nltk.corpus import stopwords
            self.stopwords = set(stopwords.words('english'))

        except Exception as e:
            print(f"NLTK nicht verfügbar: {e}")
            print("Verwende manuelle Füllwörter-Liste")
            self.stopwords = set(["like", "just", "really", "very", "actually", "basically", "literally",
                "seriously", "honestly", "obviously", "clearly", "definitely",
                "sort", "kind", "maybe", "perhaps", "possibly", "probably",
                "somewhat", "rather", "quite", "fairly", "pretty",
                "so", "such", "totally", "completely", "absolutely", "entirely",
                "extremely", "incredibly", "remarkably", "particularly",
                "then", "now", "well", "anyway", "meanwhile", "eventually",
                "somehow", "essentially", "practically", "virtually",
                "apparently", "seemingly", "supposedly", "allegedly",
                "anyhow", "fundamentally",
                "simply", "merely", "only", "hardly", "barely", "nearly",
                "and", "or", "is", "for", "the", "a", "an", "to", "in", "on", "at"])

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

        return " ".join(cleaned_words)"""