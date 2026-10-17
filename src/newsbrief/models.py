from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class Story:
    title: str 
    url: str
    source: str
    category: str 
    published_at: datetime
    summary: str = ""

@dataclass(frozen=True)
class Feed:
    name: str
    category: str
    url: str
