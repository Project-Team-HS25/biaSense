import spacy
from spacy import registry

# Trainiertes Modell laden
nlp = spacy.load("models/textcat-mini")

print("pipes:", nlp.pipe_names)
print("config sections:", list(nlp.config.keys()))

# Verfügbare Architekturen der TextCat-Modelle anzeigen
archs = registry.architectures.get_all()
print("erste Architekturen:", list(archs.keys())[:20])

# Pipeline-Struktur und Status anzeigen
print(nlp.analyze_pipes(pretty=True))

# Auszug aus der Config zeigen (zur Übersicht)
print("\nconfig (gekürzt):")
print(nlp.config.to_str()[:600])

