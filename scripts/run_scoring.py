import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from framing.config import cfg
from framing.scoring import score_folder

if __name__ == "__main__":
    print(f"Features in: {cfg.data_features_dir}")
    print(f"Scores out:  {cfg.data_scored_dir}")
    counts = score_folder(cfg.data_features_dir, cfg.data_scored_dir)
    print("Geschrieben (Scores):", counts)
