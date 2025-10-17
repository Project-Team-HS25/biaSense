# src/framing/preprocessing.py
from dataclasses import asdict
from pathlib import Path
from typing import Dict, Any, List
import json
import re
import spacy

from .config import cfg
from .schemas import PreprocessOutput
from .io_utils import write_json

# -----------------------------
# Settings / Debug
# -----------------------------
VERBOSE = True  # bei Bedarf auf False setzen

# Wort-Token-Erkennung: hat mind. einen Buchstaben (A–Z)
_WORD_RE = re.compile(r"[A-Za-z]")

_nlp = None


def _get_nlp():
    """Lazily ein spaCy-nlp Objekt laden (einmal pro Prozess)."""
    global _nlp
    if _nlp is None:
        _nlp = spacy.load(cfg.spacy_model)
        if not _nlp.has_pipe("senter"):
            try:
                _nlp.add_pipe("senter")
            except Exception:
                # senter ist optional – wenn's nicht geht, einfach weiter
                pass
    return _nlp


def _read_text_any(path: Path) -> str:
    """
    Update B: Text robust laden – mehrere Encodings versuchen.
    Verhindert, dass UTF-16/CP1252 als 'leer' gelesen wird.
    """
    raw = path.read_bytes()
    for enc in ("utf-8", "utf-8-sig", "utf-16", "utf-16-le", "utf-16-be", "cp1252"):
        try:
            return raw.decode(enc)
        except Exception:
            continue
    # Letzter Fallback: UTF-8 mit ignore (verwirft kaputte Bytes)
    return raw.decode("utf-8", errors="ignore")


def _alpha_token_count(tokens: List[str]) -> int:
    """Zähle nur Tokens, die mindestens einen Buchstaben enthalten (ignoriert reine Satzzeichen)."""
    return sum(1 for t in tokens if _WORD_RE.search(t))


def preprocess_text(text: str, text_id: str, label: str) -> PreprocessOutput:
    """Text mit spaCy analysieren und strukturierte Felder liefern."""
    nlp = _get_nlp()
    doc = nlp(text)
    return PreprocessOutput(
        id=text_id,
        label=label,
        text=text,
        tokens=[t.text for t in doc],
        lemmas=[t.lemma_ for t in doc],
        pos=[t.pos_ for t in doc],
        deps=[t.dep_ for t in doc],
        sents=[s.text.strip() for s in doc.sents],
        ents=[
            {"text": e.text, "label": e.label_, "start": e.start_char, "end": e.end_char}
            for e in doc.ents
        ],
    )


def preprocess_one(source_path: Path, text_id: str, label: str) -> Dict[str, Any]:
    """Eine Datei laden, verarbeiten und auf die gewünschten Felder reduzieren."""
    if not source_path.exists():
        raise FileNotFoundError(f"Quelle fehlt: {source_path}")
    text = _read_text_any(source_path).strip()
    data = asdict(preprocess_text(text, text_id=text_id, label=label))
    return {k: data[k] for k in cfg.keep_fields if k in data}


def preprocess_from_index(index_path: Path, out_dir: Path) -> List[Path]:
    """
    Erwartet eine JSON-Datei (Liste von Objekten) unter index_path
    mit Feldern: id, source_path, (optional) label, (optional) min_tokens.
    Schreibt pro Eintrag eine JSON nach out_dir/<id>.json
    """
    entries = json.loads(index_path.read_text(encoding="utf-8"))
    out_dir.mkdir(parents=True, exist_ok=True)
    written: List[Path] = []

    for i, row in enumerate(entries, start=1):
        src = Path(row["source_path"])
        if not src.exists():
            if VERBOSE:
                print(f"⚠️  [{i}] Datei fehlt: {src}")
            continue

        item = preprocess_one(src, text_id=row["id"], label=row.get("label", ""))

        all_tokens = len(item.get("tokens", []))
        alpha_tokens = _alpha_token_count(item.get("tokens", []))
        min_req = int(row.get("min_tokens", cfg.min_tokens))

        if VERBOSE:
            print(
                f"ℹ️  [{i}] id={row['id']} | tokens(all/alpha)={all_tokens}/{alpha_tokens} | min={min_req}"
            )

        # Filter auf Basis alphabetischer Tokens (robuster)
        if alpha_tokens < min_req:
            if VERBOSE:
                print(
                    f"⚠️  [{i}] Zu wenig Tokens (alpha={alpha_tokens} < min={min_req}), skip: id={row['id']}"
                )
            continue

        out_path = out_dir / f"{item['id']}.json"
        write_json(out_path, item)
        if VERBOSE:
            print(f"✅ [{i}] {row['id']} → {out_path.name}")
        written.append(out_path)

    return written
