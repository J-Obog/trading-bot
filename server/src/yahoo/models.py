from datetime import datetime
from enum import IntEnum
from typing import Optional
from dataclasses import dataclass

class Sentiment(IntEnum):
    BUY = 1
    SENLL = -1
    NEUTRAL = 0
    UKNOWN = -999

@dataclass
class Rating:
    sentiment: Sentiment
    price_target: Optional[float]
    announcement_date: datetime
    analyst: str
    uuid: str

@dataclass
class Tick:
    hi: float
    lo: float
    open: float
    close: float
    timestamp: datetime
