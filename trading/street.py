from datetime import datetime
from typing import List

from bs4 import BeautifulSoup
from trading.data import Holding, HoldingType, Order, OrderType
import requests

class WallStreetSurvivorClient:
    def __init__(self, cookie: str):
        self.sess = requests.Session()
        self.sess.headers["Cookie"] = cookie

    def place_trade(self, order: Order):
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

    def get_pending_orders(self) -> List[Order]:
        orders = []

        q = {
            "pageIndex": 0,
            "pageSize": 100,
            "startDate": "11-17-2023",
            "endDate": datetime.now().strftime("%m/%d/%Y"),
            "sortField": "CreateDate",
            "sortDirection": "DESC"
        }
        
        content: str = self.sess.get("https://app.wallstreetsurvivor.com/account/getorderhistory", params=q).json()["Html"]
        
        sp = BeautifulSoup(content, "html.parser")
        sp = sp.find(id="order-history-container") 

        for tr in sp.find_all("tr"):
            tds = tr.find_all("td")
            order_side = tds[3].text.split("-")[1].strip().lower()

            if tds[-1].text == "Open":
                orders.append(
                    Order(
                        quantity=int(tds[2].text),
                        symbol=tds[1].text,
                        order_type=OrderType(order_side)
                    )
                )
        
        return orders

    def get_holdings(self) -> List[Holding]:
        holdings = []

        q = {
            "securityType": "Equities",
            "pageIndex": 0,
            "pageSize": 100,
            "sortField": "CreateDate",
            "sortDirection": "DESC"
        }
        
        content: str = self.sess.get("https://app.wallstreetsurvivor.com/portfolio/openpositionsbysecuritytype", params=q).json()["Html"]

        sp = BeautifulSoup(content.replace("\r", "").replace("\n", "").replace(" ", ""), "html.parser")

        for tr in sp.find_all("tr"):
            tds = tr.find_all("td") 
            quantity = int(tds[1].text)

            holdings.append(
                Holding(
                    symbol=tds[0].text,
                    quantity=abs(quantity),
                    holding_type= (HoldingType.LONG if quantity >= 0 else HoldingType.SHORT)
                )
            )
        
        return holdings