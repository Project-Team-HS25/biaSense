import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from framing.config import cfg
from framing.feature_extraction import extract_features_folder

if __name__ == "__main__":
    print(f"Processed in:  {cfg.data_processed_dir}")
    print(f"Features out:  {cfg.data_features_dir}")
    counts = extract_features_folder(cfg.data_processed_dir, cfg.data_features_dir)
    print("Geschrieben (Features):", counts)
