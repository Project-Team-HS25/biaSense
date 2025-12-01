## **biaSense - Modulare Plattform für Sentiment- und Framing-Analyse**

### **1. Überblick und Zielsetzung**

Das **biaSense**-Projekt stellt eine mehrstufige und erweiterbare Plattform zur automatisierten Analyse von Textdokumenten hinsichtlich **Sentiment** (subjektive Stimmung) und **Framing** (zugrundeliegende Deutungsrahmen/Narrative) bereit.

Die Architektur ist in verschiedene, voneinander unabhängige Analyse-Module unterteilt (Phase 1, 2 und 3), die es ermöglichen, **verschiedene NLP-Methoden**, von simplen linguistischen Regeln bis hin zu komplexen Large Language Models (LLMs), nebeneinander zu entwickeln, zu testen und zu vergleichen. Das Haupt-Interface bildet eine interaktive **Streamlit-Webanwendung (UI)**.

### **2. Analysephasen**

| Phase | Fokus | Haupttechnologie(n) | UI-Seite |
| :--- | :--- | :--- | :--- |
| **Phase 1: Basale Analyse** | Detektion von linguistischen Merkmalen und Visualisierung von Gewichtungen. | N-Gramme, Lexika, Klassische ML-Modell-Architekturen. | `1_Phase_1_basic_Analyzer.py` und `2_Phase_1_Attention.py` |
| **Phase 2: Klassisches NLP** | Anwendung traditioneller Sentiment-Klassifikatoren und regelbasierter Frame-Erkennung. | Trainierte spaCy TextCategorizer Modelle, Manuelle/Erlernten Regelwerke. | `3_Phase_2_ML_based_Analysis.py` und `4_Phase_2_Rulelearner.py` |
| **Phase 3: LLM-Erweiterung** | Kontexteinbeziehende und interpretative Analyse komplexer Framing-Muster. | Lokal gehostetes LLM (Ollama/Phi-3). | `5_Phase_3_LLM_Analysis.py` |

-----

### **3. Erste Schritte (Quickstart)**

#### **3.1. Systemvoraussetzungen**

1.  **Python (3.x)** muss installiert sein.
2.  **Ollama**: Für die **Phase 3 (LLM-Analyse)** muss der lokale LLM-Laufzeitdienst **Ollama** installiert sein:
      * Laden Sie Ollama von [https://ollama.com/download](https://ollama.com/download) herunter.
      * Öffnen Sie ein Terminal (CMD) und laden Sie das erforderliche Modell:
        ```bash
        ollama pull phi3
        ```
        *(Warten Sie den vollständigen Download ab.)*

#### **3.2. Entwicklungsumgebung einrichten**

1.  **Repository klonen:**
    ```bash
    git clone https://github.com/Project-Team-HS25/biaSense
    cd biaSense
    ```
2.  **Virtuelle Umgebung (venv) erstellen und aktivieren:**
      * **Windows:**
        ```bash
        python -m venv .venv
        .venv\Scripts\Activate
        ```
      * **Linux / Mac:**
        ```bash
        python3 -m venv .venv
        source .venv/bin/activate
        ```
3.  **Abhängigkeiten installieren:**
    Stellen Sie sicher, dass die `venv` aktiviert ist und installieren Sie die Pakete:
    ```bash
    pip install -r requirements.txt
    py -m spacy download en_core_web_sm
    ```

#### **3.3. Starten des User Interface (UI)**

Das zentrale Interface basiert auf Streamlit und startet die Webanwendung:

```bash
py -m streamlit run Home.py
```

  * Die Anwendung öffnet sich im Browser. Navigieren Sie über das Menü an der Seite zu den verschiedenen Analyse-Phasen.
  * *Hinweis:* Das Terminal/CMD, in dem Sie den Befehl ausführen, muss geöffnet bleiben. Schließen Sie es mit `Strg + C`.

-----

### **4. Kontinuierliche Verbesserung (Nächste Schritte)**

Die folgenden Punkte sind Optionen für die Weiterentwicklung des Projekts:

  - Erweiterung der Trainingsdatenbasis für verbesserte Modellgenauigkeit. (besonders ML-Framing da der Datensatz generiert wurde)
  - Implementierung von fortgeschrittenen Evaluierungsmetriken (Cross-Validation, Confusion-Matrix) mit Bibliotheken wie scikit-learn.
  - Integration und Test von Sprachmodellen für die Analyse deutscher Texte.

-----

### **5. Häufige Probleme und Lösungen ⚙️**

| Problem | Ursache | Lösung |
| :--- | :--- | :--- |
| **`pip` Module nicht gefunden** | Die virtuelle Umgebung (`.venv`) ist nicht aktiviert. | Stellen Sie sicher, dass `.venv\Scripts\activate` (Windows) oder `source .venv/bin/activate` (Linux/Mac) ausgeführt wurde. |
| **`spacy` Modell fehlt** | Das Basis-Sprachmodell wurde nicht geladen. | Führen Sie `python -m spacy download en_core_web_sm` aus. |
| **JSONL Formatfehler** | Falsches Datenformat in Trainingsdateien. | Jede Zeile muss exakt ein gültiges JSON-Objekt sein; es sind keine Kommas zwischen den Zeilen erlaubt. |
| **Ollama/LLM-Verbindung fehlgeschlagen** | Der Ollama-Dienst läuft nicht oder das Modell ist nicht geladen. | Stellen Sie sicher, dass Ollama läuft und Sie `ollama pull phi3` erfolgreich ausgeführt haben. |
| **UI/Terminal-Blockade** | Die Anwendung wurde nicht korrekt beendet. | Beenden Sie das Terminal, in dem Streamlit läuft, mit `Strg + C`. |

