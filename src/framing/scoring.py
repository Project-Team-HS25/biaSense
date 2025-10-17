# src/framing/scoring.py
from __future__ import annotations
from pathlib import Path
from typing import Dict, Any
import json

from .config import cfg

def _read_json(p: Path) -> Dict[str, Any]:
    return json.loads(p.read_text(encoding="utf-8"))

def _write_json(p: Path, obj: Dict[str, Any]) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")

def _norm(x: float, cap: float) -> float:
    if cap <= 0: return 0.0
    return max(0.0, min(x / cap, 1.0))

def score_one(feat: Dict[str, Any]) -> Dict[str, Any]:
    """Nimmt ein Feature-Objekt (aus *.features.json) und gibt Frame-Scores 0..1 zurück."""
    c = cfg.caps
    w = cfg.weights

    # Normalisierte Inputs
    econ_d   = _norm(feat.get("economy_density", 0.0), c["density"])
    sec_d    = _norm(feat.get("security_density", 0.0), c["density"])
    moral_d  = _norm(feat.get("moral_density", 0.0), c["density"])
    conf_d   = _norm(feat.get("conflict_density", 0.0), c["density"])
    vt_d     = _norm(feat.get("victim_taeter_density", 0.0), c["density"])
    loaded_d = _norm(feat.get("loaded_adjadv_density", 0.0), c["loaded_density"])
    prim_e   = _norm(float(feat.get("primacy_econ_hits", 0)), c["primacy_hits"])
    rec_m    = _norm(float(feat.get("recency_moral_hits", 0)), c["recency_hits"])
    qratio   = _norm(feat.get("quote_ratio", 0.0), c["quote_ratio"])
    hedge    = _norm(feat.get("hedge_score_per_sent", 0.0), c["hedge_per_sent"])
    blame    = _norm(feat.get("blame_events_per_100w", 0.0), c["blame_per_100w"])

    # noch nicht implementierte Features (Platzhalter)
    polar = 0.0   # TODO: später Sentiment-Polarisation zwischen Entitäten
    passive = 0.0 # TODO: später Passiv mit Harm-Verben

    scores = {
        "economy": (
            w["economy"]["density"] * econ_d +
            w["economy"]["loaded"]  * loaded_d +
            w["economy"]["primacy"] * prim_e
        ),
        "security": (
            w["security"]["density"] * sec_d +
            w["security"]["quotes"]  * qratio +
            w["security"]["hedge"]   * hedge
        ),
        "moral": (
            w["moral"]["density"] * moral_d +
            w["moral"]["loaded"]  * loaded_d +
            w["moral"]["recency"] * rec_m
        ),
        "conflict": (
            w["conflict"]["blame"] * blame +
            w["conflict"]["polar"] * polar +
            w["conflict"]["quotes"]* qratio
        ),
        "victim_taeter": (
            w["victim_taeter"]["density"] * vt_d +
            w["victim_taeter"]["passive"] * passive
        ),
    }

    # Top-N (z.B. 2) – optional
    top = sorted(scores.items(), key=lambda kv: kv[1], reverse=True)[:2]

    return {
        "id": feat.get("id", ""),
        "label": feat.get("label", ""),
        "scores": scores,
        "top2": [{"frame": k, "score": round(v, 3)} for k, v in top],
        "norm_inputs": {  # transparent fürs Debugging
            "economy_density_n": econ_d,
            "security_density_n": sec_d,
            "moral_density_n": moral_d,
            "conflict_density_n": conf_d,
            "victim_taeter_density_n": vt_d,
            "loaded_density_n": loaded_d,
            "primacy_econ_hits_n": prim_e,
            "recency_moral_hits_n": rec_m,
            "quote_ratio_n": qratio,
            "hedge_per_sent_n": hedge,
            "blame_per_100w_n": blame,
        },
    }

def score_folder(features_root: Path, out_root: Path) -> Dict[str, int]:
    out_root.mkdir(parents=True, exist_ok=True)
    count = 0
    for p in sorted(features_root.glob("*.features.json")):
        feat = _read_json(p)
        res = score_one(feat)
        out_path = out_root / f"{res['id']}.scores.json"
        _write_json(out_path, res)
        count += 1
    return {"all": count}
