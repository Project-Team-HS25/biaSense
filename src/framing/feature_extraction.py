from __future__ import annotations
from pathlib import Path
from typing import Dict, List, Set, Any
from dataclasses import asdict
import re

from .config import cfg
from .schemas import FeatureRow
from .io_utils import read_json, write_json

_word_re = re.compile(r"[A-Za-z][A-Za-z'-]*")

def _load_list(path: Path) -> Set[str]:
    if not path.exists():
        return set()
    terms = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        terms.append(line.lower())
    return set(terms)

def _load_lexicons() -> Dict[str, Set[str]]:
    L = {
        "economy": _load_list(cfg.lexicon_dir / "economy_en.txt"),
        "security": _load_list(cfg.lexicon_dir / "security_en.txt"),
        "moral": _load_list(cfg.lexicon_dir / "moral_en.txt"),
        "conflict": _load_list(cfg.lexicon_dir / "conflict_en.txt"),
        "victim_taeter": _load_list(cfg.lexicon_dir / "victim_taeter_en.txt"),
        "hedges": _load_list(cfg.lexicon_dir / "hedges_en.txt"),
        "loaded": _load_list(cfg.lexicon_dir / "loaded_en.txt"),
        "blame_verbs": _load_list(cfg.lexicon_dir / "blame_verbs_en.txt"),
    }
    missing = [k for k,v in L.items() if not v]
    if missing:
        raise FileNotFoundError(f"Lexika fehlen/leer: {missing} unter {cfg.lexicon_dir}")
    return L

def _density(n: int, total: int) -> float:
    if total <= 0: return 0.0
    return round(100.0 * n / total, 4)

def _count_in_sents(targets: Set[str], sents: List[str]) -> int:
    hits = 0
    for s in sents:
        toks = _word_re.findall(s.lower())
        hits += sum(1 for t in toks if t in targets)
    return hits

def _quote_ratio(text: str) -> float:
    spans = re.findall(r"\"[^\"]+\"", text)
    quoted = sum(len(s) for s in spans)
    return round(quoted / max(len(text),1), 4)

def extract_features_one(item: Dict[str, Any], L: Dict[str, Set[str]]) -> FeatureRow:
    lemmas = [str(x).lower() for x in item.get("lemmas", [])]
    pos = item.get("pos", [])
    sents = item.get("sents", [])
    text = item.get("text", "")

    n_tokens = len(lemmas)
    n_sents = len(sents)

    econ = sum(1 for l in lemmas if l in L["economy"])
    sec = sum(1 for l in lemmas if l in L["security"])
    moral = sum(1 for l in lemmas if l in L["moral"])
    conf = sum(1 for l in lemmas if l in L["conflict"])
    vt = sum(1 for l in lemmas if l in L["victim_taeter"])
    hedge = sum(1 for l in lemmas if l in L["hedges"])
    loaded = sum(1 for l,p in zip(lemmas, pos) if p in ("ADJ","ADV") and l in L["loaded"])
    blame = sum(1 for l in lemmas if l in L["blame_verbs"])

    return FeatureRow(
        id=item.get("id",""),
        label=item.get("label",""),
        n_tokens=n_tokens,
        n_sents=n_sents,
        economy_density=_density(econ, n_tokens),
        security_density=_density(sec, n_tokens),
        moral_density=_density(moral, n_tokens),
        conflict_density=_density(conf, n_tokens),
        victim_taeter_density=_density(vt, n_tokens),
        hedge_score_per_sent=round(hedge / max(n_sents,1), 4),
        loaded_adjadv_density=_density(loaded, n_tokens),
        quote_ratio=_quote_ratio(text),
        primacy_econ_hits=_count_in_sents(L["economy"], sents[:2] if n_sents>=2 else sents),
        recency_moral_hits=_count_in_sents(L["moral"], sents[-2:] if n_sents>=2 else sents),
        blame_events_per_100w=round(100.0 * blame / max(n_tokens,1), 4),
    )

def extract_features_folder(processed_root: Path, out_root: Path) -> Dict[str,int]:
    L = _load_lexicons()
    out_root.mkdir(parents=True, exist_ok=True)
    count = 0
    for p in sorted(processed_root.glob("*.json")):
        item = read_json(p)
        row = extract_features_one(item, L)
        write_json(out_root / f"{row.id}.features.json", asdict(row))
        count += 1
    return {"all": count}
