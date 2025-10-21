# Sentiment Analysis with NLTK

from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *

import nltk

nltk.download('subjectivity')
nltk.download('vader_lexicon')
nltk.download('punkt')

# Anzahl der Dokumente
n_instances = 100
subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]

# Split in Training und Testdaten (balanced)
train_subj_docs = subj_docs[:80]
test_subj_docs = subj_docs[80:100]
train_obj_docs = obj_docs[:80]
test_obj_docs = obj_docs[80:100]

training_docs = train_subj_docs + train_obj_docs
testing_docs = test_subj_docs + test_obj_docs

# Sentiment Analyzer initialisieren
sentim_analyzer = SentimentAnalyzer()
all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])

# Feature-Extraktion (Unigramme mit Mindesthäufigkeit)
unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)

# Feature-Darstellung anwenden
training_set = sentim_analyzer.apply_features(training_docs)
test_set = sentim_analyzer.apply_features(testing_docs)

# Klassifikator trainieren
trainer = NaiveBayesClassifier.train
classifier = sentim_analyzer.train(trainer, training_set)

# Auswertung
results = sentim_analyzer.evaluate(test_set)
for key, value in sorted(results.items()):
    print(f"{key}: {value}")

# ------------------------------------------------------------
# VADER Sentiment Analysis
# ------------------------------------------------------------

from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk import tokenize

sentences = [
    "VADER is smart, handsome, and funny.",
    "Vader is shity, stupid, and ugly.",

]

paragraph = (
    "It was one of the worst movies I've seen, despite good reviews. "
    "Unbelievably bad acting!! Poor direction. VERY poor production. "
    "The movie was bad. Very bad movie. VERY bad movie. VERY BAD movie. VERY BAD movie!"
)

lines_list = tokenize.sent_tokenize(paragraph)
sentences.extend(lines_list)

sid = SentimentIntensityAnalyzer()

for sentence in sentences:
    ss = sid.polarity_scores(sentence)
    print(sentence)
    for k in sorted(ss):
        print(f"  {k}: {ss[k]}")
    print()