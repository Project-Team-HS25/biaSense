#Business Logic - Textanalyse
import csv
import os

class TextAnalyzer:
    def __init__(self):
        self.stopwords = None
        self.use_spacy = False
        self.adjectives = {}
        self.verbs = {}
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

        try:
            csv_path = os.path.join("business_logic", "verbs.csv")
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    verb = row['verb'].strip().lower()
                    score = int(row['score'])
                    self.verbs[verb] = score
        except FileNotFoundError:
            print(f"Die Datei verbs.csv konnte nicht gefunden werden.")
            self.verbs = {}

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
        adjective_counts = {}

        for word in words:
            word_clean = word.lower().strip('.,!?;:')
            if word_clean in self.adjectives:
                score = self.adjectives[word_clean]
                if word_clean in adjective_counts:
                    adjective_counts[word_clean]['count'] += 1
                else:
                    adjective_counts[word_clean] = {'score': score, 'count': 1}

        # Konvertiere in Liste von Tupeln (adjektiv, score, count)
        found_adjectives = [(adj, data['score'], data['count'])
                            for adj, data in adjective_counts.items()]

        # Durchschnitt berechnen (score gewichtet mit Häufigkeit)
        if found_adjectives:
            total_score = sum(score * count for _, score, count in found_adjectives)
            total_count = sum(count for _, _, count in found_adjectives)
            avg_score = total_score / total_count

            # Sentiment bestimmen
            if avg_score >= 60:
                sentiment = "positiv"
            elif avg_score >= 40:
                sentiment = "neutral"
            else:
                sentiment = "negativ"
        else:
            avg_score = 50
            sentiment = "neutral"

        return {
            'found_adjectives': found_adjectives,
            'average_score': round(avg_score, 1),
            'sentiment': sentiment,
            'count': len(adjective_counts)
        }

    def analyze_verbs(self, text):
        words = text.split()
        verb_counts = {}

        for word in words:
            word_clean = word.lower().strip('.,!?;:')
            if word_clean in self.verbs:
                score = self.verbs[word_clean]
                if word_clean in verb_counts:
                    verb_counts[word_clean]['count'] += 1
                else:
                    verb_counts[word_clean] = {'score': score, 'count': 1}

        found_verbs = [(verb, data['score'], data['count'])
                       for verb, data in verb_counts.items()]

        if found_verbs:
            total_score = sum(score * count for _, score, count in found_verbs)
            total_count = sum(count for _, _, count in found_verbs)
            avg_score = total_score / total_count

            if avg_score >= 60:
                sentiment = "positiv"
            elif avg_score >= 40:
                sentiment = "neutral"
            else:
                sentiment = "negativ"
        else:
            avg_score = 50
            sentiment = "neutral"

        return {
            'found_verbs': found_verbs,
            'average_score': round(avg_score, 1),
            'sentiment': sentiment,
            'count': len(verb_counts)
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