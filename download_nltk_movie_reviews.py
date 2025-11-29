import ssl
import nltk

# --- SSL-Workaround: Zertifikatsprüfung für diesen Prozess deaktivieren ---
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Falls Python zu alt ist, einfach nichts tun
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# --- NLTK-Corpus herunterladen ---
# Optionaler Zielordner; einer der Pfade, die NLTK sowieso durchsucht
download_dir = "/Users/tanjaluscher/nltk_data"

nltk.download('movie_reviews', download_dir=download_dir)

print("Fertig: movie_reviews wurde heruntergeladen nach", download_dir)