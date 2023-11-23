import requests
from trading.data import StockRatingType

ANALYST_API_URL = "https://api.nasdaq.com/api/analyst"
URL = "https://stockanalysis.com/list/biggest-companies/"
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"

def to_rating(nasdaq_rating_str: str) -> StockRatingType:
    return {
        "Strong Buy": StockRatingType.BUY,
        "Buy": StockRatingType.BUY,
        "Strong Sell": StockRatingType.SELL,
        "Sell": StockRatingType.SELL,
        "Underperform": StockRatingType.SELL,
        "Hold": StockRatingType.HOLD
    }[nasdaq_rating_str]

class NasdaqClient:
    def __init__(self):
        self.sess = requests.Session()
        self.sess.headers["User-Agent"] = USER_AGENT

    def get_rating(self, symbol: str) -> StockRatingType:
        data = self.sess.get(f"{ANALYST_API_URL}/{symbol}/ratings").json()["data"]
        
        return to_rating(data["meanRatingType"])
    