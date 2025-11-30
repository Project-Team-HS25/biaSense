import ssl
import nltk
import os
from pathlib import Path
import sys

# ----------------------------------------------------
# 1. SETUP & PFADE (OS-UNABHÄNGIG)
# ----------------------------------------------------
# Bestimme das Verzeichnis, in dem dieses Skript liegt
current_dir = Path(__file__).parent

# Erstelle einen lokalen Ordner für NLTK Daten im Projektverzeichnis
# Das macht es unabhängig vom User-Ordner
nltk_data_dir = current_dir / "nltk_data"
nltk_data_dir.mkdir(parents=True, exist_ok=True)

# Füge diesen Pfad zu NLTK hinzu, damit es weiß, wo es speichern soll
nltk.data.path.append(str(nltk_data_dir))

# Explizites Encoding für Print-Ausgaben setzen, falls möglich, 
# oder einfach ASCII verwenden (sicherste Variante für Windows).
print(f"Zielverzeichnis fuer Daten: {nltk_data_dir}")

# ----------------------------------------------------
# 2. SSL-WORKAROUND
# ----------------------------------------------------
# Zertifikatsprüfung für diesen Prozess deaktivieren (hilft oft in Firmennetzwerken oder Mac)
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Falls Python zu alt ist, einfach nichts tun
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

# ----------------------------------------------------
# 3. DOWNLOAD
# ----------------------------------------------------
print("Starte Download von 'movie_reviews'...")

# Wir laden 'movie_reviews' und 'punkt' (wichtig für Tokenizer) in unser lokales Verzeichnis
try:
    nltk.download('movie_reviews', download_dir=str(nltk_data_dir))
    nltk.download('punkt', download_dir=str(nltk_data_dir))
    nltk.download('punkt_tab', download_dir=str(nltk_data_dir)) # Neuere NLTK Versionen brauchen dies manchmal
    
    # ASCII-sichere Erfolgsmeldung (keine Emojis)
    print("\n[OK] Erfolg: Daten wurden erfolgreich heruntergeladen.")
    print(f"Du kannst nun die App starten. Die Daten liegen in: {nltk_data_dir}")
    
except Exception as e:
    # ASCII-sichere Fehlermeldung
    print(f"\n[FEHLER] Fehler beim Download: {e}")