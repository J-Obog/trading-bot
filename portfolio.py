from enum import IntEnum
import requests
from dataclasses import dataclass

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
    def __init__(self, auth_token, portfolio_id):
        self.sess = requests.Session()
        self.sess.headers["Cookie"] = f".WSS-Auth={auth_token};__WallStreetSurvivorProd=TournamentID={portfolio_id}" 

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

        self.sess.post(BASE_ORDER_API_URI, data=payload)
