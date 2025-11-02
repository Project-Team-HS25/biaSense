#Business Logic - Textanalyse
import csv
import os

class TextAnalyzer:
    def __init__(self):
        self.adjectives = {}
        self.verbs = {}
        self.irregular_verbs = {}
        self.irregular_adjectives = {}
        self.stopwords = set()

        # Lade alle CSV-Dateien
        self.load_stopwords()
        self.load_irregular_verbs()
        self.load_irregular_adjectives()
        self.load_adjectives()
        self.load_verbs()

        # Initialisiere Suffix-Regeln
        self._initialize_suffix_rules()

    def load_stopwords(self):
        """Lädt Stopwords aus CSV oder verwendet Default"""
        try:
            csv_path = os.path.join("business_logic", "CSV-Data", "stopwords.csv")
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.stopwords.add(row['word'].strip().lower())
            print(f"Stopwords geladen: {len(self.stopwords)} Wörter")
        except FileNotFoundError:
            # Default Stopwords
            self.stopwords = {
                "like", "just", "really", "very", "actually", "basically", "literally",
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
                "and", "or", "is", "am", "are", "was", "were", "been", "being",
                "for", "the", "a", "an", "to", "in", "on", "at", "of", "with"
            }
            print("Verwende Standard-Stopwords")

    def load_irregular_verbs(self):
        """Lädt unregelmäßige Verben aus CSV"""
        try:
            csv_path = os.path.join("business_logic", "CSV-Data", "lemma_verbs.csv")
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    form = row['form'].strip().lower()
                    lemma = row['lemma'].strip().lower()
                    self.irregular_verbs[form] = lemma
            print(f"Unregelmäßige Verben geladen: {len(self.irregular_verbs)} Formen")
        except FileNotFoundError:
            print("Datei lemma_verbs.csv nicht gefunden - verwende leeres Wörterbuch")
            self.irregular_verbs = {}

    def load_irregular_adjectives(self):
        """Lädt unregelmäßige Adjektive aus CSV"""
        try:
            csv_path = os.path.join("business_logic", "CSV-Data", "lemma_adjectives.csv")
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    form = row['form'].strip().lower()
                    lemma = row['lemma'].strip().lower()
                    self.irregular_adjectives[form] = lemma
            print(f"Unregelmäßige Adjektive geladen: {len(self.irregular_adjectives)} Formen")
        except FileNotFoundError:
            print("Datei lemma_adjectives.csv nicht gefunden - verwende leeres Wörterbuch")
            self.irregular_adjectives = {}

    def load_adjectives(self):
        """Lädt Adjektive mit Sentiment-Scores"""
        try:
            csv_path = os.path.join("business_logic", "CSV-Data", "adjectives.csv")
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    adjective = row['adjective'].strip().lower()
                    score = int(row['score'])
                    self.adjectives[adjective] = score
            print(f"Adjektive geladen: {len(self.adjectives)} Wörter")
        except FileNotFoundError:
            print("Datei adjectives.csv nicht gefunden")
            self.adjectives = {}

    def load_verbs(self):
        """Lädt Verben mit Sentiment-Scores"""
        try:
            csv_path = os.path.join("business_logic", "CSV-Data", "verbs.csv")
            with open(csv_path, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    verb = row['verb'].strip().lower()
                    score = int(row['score'])
                    self.verbs[verb] = score
            print(f"Verben geladen: {len(self.verbs)} Wörter")
        except FileNotFoundError:
            print("Datei verbs.csv nicht gefunden")
            self.verbs = {}

    def _initialize_suffix_rules(self):
        """Initialisiert Suffix-Regeln"""
        self.consonants = set('bcdfghjklmnpqrstvwxyz')
        self.vowels = set('aeiou')

    def lemmatize(self, word):
        """
        Lemmatisieren eines einzelnen Wortes.
        1. Prüft CSV-Wörterbücher (unregelmäßige Formen)
        2. Wendet Suffix-Regeln an (regelmäßige Formen)
        """
        word_clean = word.lower().strip('.,!?;:')

        if not word_clean:
            return word_clean

        # Prüfe CSV-Wörterbücher zuerst
        if word_clean in self.irregular_verbs:
            return self.irregular_verbs[word_clean]

        if word_clean in self.irregular_adjectives:
            return self.irregular_adjectives[word_clean]

        # Wende Suffix-Regeln an
        return self._apply_suffix_rules(word_clean)

    def _apply_suffix_rules(self, word):
        """
        Wendet Suffix-Regeln für regelmäßige Wortformen an.
        Diese bleiben im Code, da sie algorithmisch sind.
        """
        if len(word) <= 3:
            return word

        # -ies -> -y
        if word.endswith('ies') and len(word) > 4:
            return word[:-3] + 'y'

        # -iest -> -y
        if word.endswith('iest') and len(word) > 5:
            return word[:-4] + 'y'

        # -ier -> -y
        if word.endswith('ier') and len(word) > 4:
            return word[:-3] + 'y'

        # -ing
        if word.endswith('ing') and len(word) > 5:
            stem = word[:-3]

            # Verdoppelte Konsonanten
            if len(stem) >= 2 and stem[-1] == stem[-2] and stem[-1] in self.consonants:
                return stem[:-1]

            # Stummes -e
            if stem[-1] in self.consonants and len(stem) >= 2:
                if stem[-2] in self.vowels and stem[-1] in {'v', 'k', 'c', 't', 'z'}:
                    return stem + 'e'

            return stem if len(stem) >= 3 else word

        # -ed
        if word.endswith('ed') and len(word) > 4:
            stem = word[:-2]

            # Verdoppelte Konsonanten
            if len(stem) >= 2 and stem[-1] == stem[-2] and stem[-1] in self.consonants:
                return stem[:-1]

            # -ied -> -y
            if stem.endswith('i'):
                return stem[:-1] + 'y'

            # Stummes -e
            if len(stem) >= 2 and stem[-1] in self.consonants and stem[-2] in self.vowels:
                if stem[-1] in {'v', 'c', 'g', 'z'}:
                    return stem + 'e'

            return stem if len(stem) >= 3 else word

        # -est
        if word.endswith('est') and len(word) > 5:
            stem = word[:-3]

            # Verdoppelte Konsonanten
            if len(stem) >= 2 and stem[-1] == stem[-2] and stem[-1] in self.consonants:
                return stem[:-1]

            return stem

        # -er
        if word.endswith('er') and len(word) > 4:
            stem = word[:-2]

            # Verdoppelte Konsonanten
            if len(stem) >= 2 and stem[-1] == stem[-2] and stem[-1] in self.consonants:
                return stem[:-1]

            # Aber nicht bei -eer, -ier, etc.
            if len(stem) >= 2 and stem[-1] in {'e', 'i', 'w'}:
                return word

            return stem if len(stem) >= 3 else word

        # -s (Plural/3. Person)
        if word.endswith('s') and not word.endswith('ss') and len(word) > 3:
            if word.endswith('es') and len(word) > 4:
                if word[-3:-2] in ['s', 'x', 'z'] or word[-4:-2] in ['sh', 'ch']:
                    return word[:-2]

            return word[:-1]

        return word

    def lemmatize_text(self, text):
        """Lemmatisieren eines kompletten Textes"""
        words = text.split()
        return [(word, self.lemmatize(word)) for word in words]

    def extract_filler_words(self, text):
        """Extrahiert Füllwörter"""
        word_lemmas = self.lemmatize_text(text)
        return [original for original, lemma in word_lemmas if lemma in self.stopwords]

    def remove_filler_words(self, text):
        """Entfernt Füllwörter"""
        word_lemmas = self.lemmatize_text(text)
        cleaned_words = [original for original, lemma in word_lemmas if lemma not in self.stopwords]
        return " ".join(cleaned_words)

    def analyze_adjectives(self, text):
        """Analysiert Adjektive im Text mit Lemmatisierung"""
        word_lemmas = self.lemmatize_text(text)
        adjective_counts = {}

        for original, lemma in word_lemmas:
            if lemma in self.adjectives:
                score = self.adjectives[lemma]
                if lemma in adjective_counts:
                    adjective_counts[lemma]['count'] += 1
                    adjective_counts[lemma]['originals'].add(original)
                else:
                    adjective_counts[lemma] = {
                        'score': score,
                        'count': 1,
                        'originals': {original}
                    }

        found_adjectives = [
            (lemma, data['score'], data['count'], ', '.join(sorted(data['originals'])))
            for lemma, data in adjective_counts.items()
        ]

        if found_adjectives:
            total_score = sum(score * count for _, score, count, _ in found_adjectives)
            total_count = sum(count for _, _, count, _ in found_adjectives)
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
            'found_adjectives': found_adjectives,
            'average_score': round(avg_score, 1),
            'sentiment': sentiment,
            'count': len(adjective_counts)
        }

    def analyze_verbs(self, text):
        """Analysiert Verben im Text mit Lemmatisierung"""
        word_lemmas = self.lemmatize_text(text)
        verb_counts = {}

        for original, lemma in word_lemmas:
            if lemma in self.verbs:
                score = self.verbs[lemma]
                if lemma in verb_counts:
                    verb_counts[lemma]['count'] += 1
                    verb_counts[lemma]['originals'].add(original)
                else:
                    verb_counts[lemma] = {
                        'score': score,
                        'count': 1,
                        'originals': {original}
                    }

        found_verbs = [
            (lemma, data['score'], data['count'], ', '.join(sorted(data['originals'])))
            for lemma, data in verb_counts.items()
        ]

        if found_verbs:
            total_score = sum(score * count for _, score, count, _ in found_verbs)
            total_count = sum(count for _, _, count, _ in found_verbs)
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
        """Gibt eine Sentiment-Kategorie basierend auf einem Score zurück"""
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



""" Stopwords mit saCy, Verb und Adjektiv Sentiment-Analyse mit CSV-DB aber ohne Lemmatisierung
class TextAnalyzer:
    def __init__(self):
        self.stopwords = None
        self.use_spacy = False
        self.adjectives = {}
        self.verbs = {}
        self._initialize_lemmatization()

        #Füllwörter aus spaCy laden
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

        #Adjektive aus CSV-DB laden
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

        #Verben aus CSV-DB laden
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
            return "sehr negativ"""