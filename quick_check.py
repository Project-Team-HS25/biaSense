# quick_check.py
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent  # Projekt-Root
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))  # <-- geändert

print("ROOT in sys.path?", str(ROOT) in sys.path)
print("Repo exists?", Path("data_access/repositories/news_repository.py").exists())

from business_logic.services.news_service import NewsService  # bleibt gleich

svc = NewsService()
rows = svc.build_dataset()
print(f"Samples: {len(rows)}")
print(rows[0].keys())
print(rows[0]["tone"], rows[0]["filename"])
