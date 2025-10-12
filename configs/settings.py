# configs/settings.py
# <-- geändert: BaseSettings kommt jetzt aus pydantic_settings
from pydantic_settings import BaseSettings  # <-- geändert
from pathlib import Path

class Settings(BaseSettings):
    project_root: Path = Path(".").resolve()
    data_dir: Path = project_root / "data"
    raw_dir: Path = data_dir / "raw"
    metadata_dir: Path = data_dir / "metadata"
    metadata_file: Path = metadata_dir / "apple_vision_pro_metadata_with_filenames.json"
    seed: int = 42

    class Config:
        env_prefix = "APP_"
