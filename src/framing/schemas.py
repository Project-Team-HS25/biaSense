from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class PreprocessOutput:
    id: str
    label: str
    text: str
    tokens: List[str]
    lemmas: List[str]
    pos: List[str]
    deps: List[str]
    sents: List[str]
    ents: List[Dict[str, Any]]

@dataclass
class FeatureRow:
    id: str
    label: str
    n_tokens: int
    n_sents: int
    economy_density: float
    security_density: float
    moral_density: float
    conflict_density: float
    victim_taeter_density: float
    hedge_score_per_sent: float
    loaded_adjadv_density: float
    quote_ratio: float
    primacy_econ_hits: int
    recency_moral_hits: int
    blame_events_per_100w: float
