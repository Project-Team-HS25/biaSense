# domain_model/news_metadata.py
from typing import List, Literal
from pydantic import BaseModel, HttpUrl, Field

Tone = Literal["positive", "neutral", "negative"]

class NewsMetadata(BaseModel):
    id: int
    title: str
    source: str
    url: HttpUrl
    tone: Tone
    topic: str
    summary: str
    keywords: List[str] = Field(default_factory=list)
    filename: str  # z. B. "apple_vision_pro.txt"
