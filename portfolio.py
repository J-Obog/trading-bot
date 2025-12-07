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


class OrderSide(IntEnum):
    BUY = 1
    SELL = 2

class OrderType(IntEnum):
    MARKET = 1

@dataclass
class OrderRequest:
    ticker: str
    quantity: int
    side: OrderSide
    type: OrderType


BASE_ORDER_API_URI = "https://app.wallstreetsurvivor.com/trading/placeorder"

class PortfolioApi:
    def __init__(self):
        self.sess = requests.Session()

    def execute_order(self, req: OrderRequest):
        payload = {
            "OrderSide": req.side.value, 
            "Symbol": req.ticker.upper(),
            "Quantity": req.quantity, 
            "OrderType": req.type.value,
            "Currency": "USD", 
            "SecurityType": "Equities",
            "Exchange": 1
        }        
