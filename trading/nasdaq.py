from typing import Optional
import requests

from trading.data import StockRating, StockRatingType

ANALYST_API_URL = "https://api.nasdaq.com/api/analyst"

class NasdaqClient:
    def __init__(self):
        self.sess = requests.Session()

    def get_rating(self, symbol: str) -> Optional[StockRating]:
        data = self.sess.get(f"{ANALYST_API_URL}/{symbol}/ratings").json()["data"]
        
        return StockRating(
            rating=StockRatingType(data["meanRatingType"]),
            rating_entities=set()
        )