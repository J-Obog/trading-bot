from abc import ABC

from trading.data import StockRatingType

class StockClient(ABC):
    def get_rating(self, ticker: str) -> StockRatingType:
        ...