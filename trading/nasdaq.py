from typing import Optional
import requests

from trading.data import StockRating

class NasdaqClient:
    def __init__(self):
        self.sess = requests.Session()

    def get_rating(self, symbol: str) -> Optional[StockRating]:
        foo = self.sess.get(f"https://api.nasdaq.com/api/analyst/{symbol}/ratings").json()  
        return None