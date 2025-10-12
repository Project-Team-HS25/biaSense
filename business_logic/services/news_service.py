# business_logic/services/news_service.py

from __future__ import annotations

from pathlib import Path
import sys

# Projekt-Root ermitteln (2 Ordner über services/ hinaus)
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from typing import List, Dict, Any, Optional
from sklearn.model_selection import train_test_split  # optional, für Splits
from data_access.repositories.news_repository import NewsRepository
from configs.settings import Settings

class NewsService:
    def __init__(self, repo: Optional[NewsRepository] = None, settings: Optional[Settings] = None):
        self.settings = settings or Settings()
        self.repo = repo or NewsRepository(self.settings)

    def build_dataset(self) -> List[Dict[str, Any]]:
        rows: List[Dict[str, Any]] = []
        for meta, text in self.repo.iter_samples():
            rows.append({
                "id": meta.id,
                "title": meta.title,
                "source": meta.source,
                "url": str(meta.url),
                "tone": meta.tone,
                "topic": meta.topic,
                "summary": meta.summary,
                "keywords": meta.keywords,
                "filename": meta.filename,
                "text": text
            })
        return rows

    def train_val_test_split(
        self,
        test_size: float = 0.2,
        val_size: float = 0.1,
        random_state: Optional[int] = None,
        stratify_by_tone: bool = True
    ):
        data = self.build_dataset()
        y = [r["tone"] for r in data] if stratify_by_tone else None

        trainval, test = train_test_split(
            data, test_size=test_size, random_state=random_state or self.settings.seed,
            stratify=y if stratify_by_tone else None
        )

        y_trainval = [r["tone"] for r in trainval] if stratify_by_tone else None
        val_ratio = val_size / (1.0 - test_size)

        train, val = train_test_split(
            trainval, test_size=val_ratio, random_state=random_state or self.settings.seed,
            stratify=y_trainval if stratify_by_tone else None
        )
        return train, val, test
