from typing import Optional, TypedDict, NotRequired
from bson import ObjectId
from datetime import datetime
from enum import IntEnum

class Sentiment(IntEnum):
    BULLISH = 1
    BEARISH = 2

class Outcome(IntEnum):
    CORRECT = 1
    WRONG = 2

class Analyst(TypedDict):
    _id: NotRequired[ObjectId]
    name: str

class Prediction(TypedDict):
    _id: NotRequired[ObjectId]
    analyst_id: ObjectId
    price_target: float
    date: datetime
    ticker: str
    sentiment: Sentiment
    outcome: Optional[Outcome]