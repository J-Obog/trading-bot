from datetime import datetime
from enum import IntEnum
from typing import List, Optional
import requests
from dataclasses import dataclass
from dateutil.parser import parse

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


BASE_API_URI = "https://query1.finance.yahoo.com/v2/ratings/"
BASE_URI = "https://query2.finance.yahoo.com/v8/finance/chart"

HEADERS = {
    "User-Agent": "StockAnalysis/1.0"
}

STANDARD_QUERY_PARAMS = {
    "includePrePost":"true",
    "events":"div%7Csplit%7Cearn",
    "lang":"en-US",
    "region":"US"
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

    def get_ticks(self, ticker: str, t1: datetime, t2: datetime) -> List[Tick]:
        query_params = STANDARD_QUERY_PARAMS
        query_params["period1"] = int(t1.timestamp())
        query_params["period2"] = int(t2.timestamp())
        query_params["interval"] = "1d"
        
        res = requests.get(f"{BASE_URI}/{ticker}", headers=HEADERS, params=query_params)
        data = res.json()["chart"]["result"][0]
        indicators = data["indicators"]["quote"][0]

        timestamps = datetime.fromtimestamp( data["timestamp"])
        closes = indicators["close"]
        highs = indicators["high"]
        lows = indicators["low"]

        ticks: List[Tick] = []

        for i in range(len(timestamps)):
            tick = Tick(
                    timestamp=timestamps[i],
                    close=closes[i],
                    low=lows[i], 
                    high=highs[i]
                )

            ticks.append(tick)

        return ticks
    
    def get_ratings(self, ticker: str) -> List[Rating]:
        params = BASE_QUERY_PARAMS
        params["symbol"] = ticker.upper()
        ratings = []

        res = requests.get(BASE_API_URI, params=params, headers=HEADERS).json()

        for item in res["items"]:
            raw_sentiment = item["rating_sentiment"] if ("rating_sentiment" in item) and (item["rating_sentiment"] is not None) else None
            ratings.append(
                Rating(
                    sentiment= Sentiment(raw_sentiment) if raw_sentiment is not None else Sentiment.UKNOWN,
                    price_target=item["pt_current"],
                    uuid=item["uuid"],
                    analyst=item["analyst"],
                    announcement_date=parse(item["announcement_date"], ignoretz=True)
                )
            )

        return ratings

