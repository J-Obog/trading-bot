from typing import List
from trading.data import Holding, Order
import requests

class WallStreetSurvivorClient:
    def __init__(self, cookie: str):
        self.sess = requests.Session()
        self.sess.headers["Cookie"] = cookie

    def make_order(self, order: Order):
        data = {
            "OrderSide": 1,
            "Symbol": order.symbol,
            "Quantity": order.quantity,
            "OrderType": 1, 
            "SecurityType": "Equities",
            "Currency": "USD",
            "Exchange": 1
        }   

        r = self.sess.post("https://app.wallstreetsurvivor.com/trading/placeorder", data=data).json()
        return r["Success"] == True


    def get_holdings(self) -> List[Holding]:
        return []