from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal

@dataclass(frozen=True)
class Story:
    title: str 
    url: str
    source: str
    category: str 
    published_at: datetime
    summary: str = ""
    sentiment: str | None = None
    sentiment_score: float | None = None

@dataclass(frozen=True)
class Feed:
    name: str
    category: str
    url: str

@dataclass(frozen=True)
class ExchangeRate:
    rate_date: date
    base_currency: str
    quote_currency: str
    value: Decimal
    source_url: str
