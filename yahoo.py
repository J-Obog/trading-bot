from datetime import datetime
from enum import IntEnum
from typing import List, Optional
import requests
from dataclasses import dataclass

class Sentiment(IntEnum):
    BUY = 1
    SELL = -1
    NEUTRAL = 0

@dataclass
class Rating:
    sentiment: Sentiment
    price_target: Optional[float]
    announcement_date: datetime
    analyst: str
    uuid: str


BASE_API_URI = "https://query1.finance.yahoo.com/v2/ratings/"
HEADERS = {
    "User-Agent": "StockAnalysis/1.0"
}

BASE_QUERY_PARAMS = {
    "limit": 100,
    "offset": 0,
    "order_by": "fin_score",
    "exclude_noncurrent": True, 
    "region":"US",
    "lang":"en-US",
    "desc":True,
}

class YahooApi:
    def __init__(self):
        pass

    def get_ratings(self, ticker: str) -> List[Rating]:
        params = BASE_QUERY_PARAMS
        params["symbol"] = ticker.upper()
        ratings = []

        res = requests.get(BASE_API_URI, params=params, headers=HEADERS).json()

        for item in res["items"]:
            ratings.append(
                Rating(
                    sentiment=Sentiment(item["rating_sentiment"]),
                    price_target=item["pt_current"],
                    uuid=item["uuid"],
                    analyst=item["analyst"]
                )
            )

        return ratings

