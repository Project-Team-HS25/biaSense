import os
import pandas as pd
import shutil
import input_helper
import nltk
from nltk.corpus import stopwords

#dieser Codeblock lädt die nötigen nltk Resourcen herunter (nur einmalig notwendig)
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")

inputtext = input_helper.input_valid_string("Bitte Text übermitteln:")

# Mit spacy library ----------------------------------------------------------------------------------------
import spacy
nlp = spacy.load("en_core_web_sm")
doc = nlp(inputtext.lower())
filtered = [token.text for token in doc if not token.is_stop and token.is_alpha]
print(filtered)
#-----------------------------------------------------------------------------------------------------------
