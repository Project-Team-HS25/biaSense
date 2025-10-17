from dataclasses import dataclass
from pathlib import Path

@dataclass
class PreprocessConfig:
    # NLP
    language: str = "en"
    spacy_model: str = "en_core_web_sm"
    min_tokens: int = 1

    # Pfade
    repo_root: Path = Path(__file__).resolve().parents[2]
    data_raw_dir: Path = repo_root / "data" / "raw"
    data_processed_dir: Path = repo_root / "data" / "processed"
    data_features_dir: Path = repo_root / "data" / "processed_features"
    data_scored_dir: Path = repo_root / "data" / "scored"               # <— neu
    metadata_dir: Path = repo_root / "data" / "metadata"
    index_path: Path = metadata_dir / "dataset_index.json"
    lexicon_dir: Path = repo_root / "data" / "lexicons"

    keep_fields: tuple = (
        "id","label","text","tokens","lemmas","pos","deps","sents","ents"
    )

    # --- Heuristik-Parameter (Caps/Weights) ---
    # Normalisierung: norm(x, cap) = min(x / cap, 1.0)
    caps = {
        "density": 5.0,              # per 100 Wörter
        "loaded_density": 3.0,       # per 100 Wörter
        "primacy_hits": 3.0,
        "recency_hits": 3.0,
        "quote_ratio": 0.4,
        "hedge_per_sent": 0.8,
        "blame_per_100w": 5.0,
    }

    # Gewichte pro Frame (Summe ~1.0)
    weights = {
        "economy":        {"density": 0.6, "loaded": 0.2, "primacy": 0.2},
        "security":       {"density": 0.5, "quotes": 0.3, "hedge": 0.2},
        "moral":          {"density": 0.6, "loaded": 0.2, "recency": 0.2},
        "conflict":       {"blame": 0.5, "polar": 0.3, "quotes": 0.2},  # polar hier dummy=0 (noch nicht berechnet)
        "victim_taeter":  {"density": 0.6, "passive": 0.4},             # passive hier dummy=0 (optional später)
    }

cfg = PreprocessConfig()
