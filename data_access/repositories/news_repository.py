from __future__ import annotations
from pathlib import Path
import json
from typing import List, Iterable
from pydantic import ValidationError

from domain_model.news_metadata import NewsMetadata
from configs.settings import Settings

class NewsRepository:
    def __init__(self, settings: Settings | None = None):
        self.settings = settings or Settings()
        self.raw_dir: Path = self.settings.raw_dir
        self.metadata_path: Path = self.settings.metadata_file

    # Laden aller Metadaten-Eintraege
    def load_metadata(self) -> List[NewsMetadata]:
        if not self.metadata_path.exists():
            raise FileNotFoundError(f"Metadata file not found: {self.metadata_path}")
        data = json.loads(self.metadata_path.read_text(encoding="utf-8"))
        try:
            items = [NewsMetadata(**item) for item in data]
        except ValidationError as e:
            # Bewusst explizite Fehlermeldung fuer sauberes Debugging
            raise ValueError(f"Invalid metadata format: {e}")  # noqa: E501
        return items

    # Rohtext zu einem Metadateneintrag laden
    def read_raw_text(self, tone: str, filename: str) -> str:
        # erwartet Struktur: data/raw/<tone>/<filename>
        p = self.raw_dir / tone / filename
        if not p.exists():
            raise FileNotFoundError(f"Raw text not found: {p}")
        return p.read_text(encoding="utf-8")

    # Hilfsfunktion: Iterator ueber (meta, text)
    def iter_samples(self) -> Iterable[tuple[NewsMetadata, str]]:
        for meta in self.load_metadata():
            text = self.read_raw_text(meta.tone, meta.filename)
            yield meta, text
