from typing import TypedDict, NotRequired
from bson import ObjectId
from datetime import datetime
from enum import IntEnum

class Sentiment(IntEnum):
    BULLISH = 1
    BEARISH = 2
    NEUTRAL = 3

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