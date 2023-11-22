from datetime import datetime
from typing import List

from bs4 import BeautifulSoup
from trading.data import Holding, HoldingType, Order, OrderType
import requests

API_URL = "https://app.wallstreetsurvivor.com"
PLACE_ORDER_API_URL = API_URL + "/trading/placeorder"

def order_side_from_order_type(order_type: OrderType) -> int:
    return {
        OrderType.BUY: 1,
        OrderType.SELL: 2,
        OrderType.SHORT: 3,
        OrderType.BUY_TO_COVER: 4
    }[order_type]
 
class WallStreetSurvivorClient:
    def __init__(self, cookie: str):
        self.sess = requests.Session()
        self.sess.headers["Cookie"] = cookie

    def place_order(self, order: Order):
        data = {
            "OrderSide": order_side_from_order_type(order.order_type),
            "Symbol": order.symbol,
            "Quantity": order.quantity,
            "OrderType": 1, 
            "SecurityType": "Equities",
            "Currency": "USD",
            "Exchange": 1
        }   

        r = self.sess.post("https://app.wallstreetsurvivor.com/trading/placeorder", data=data).json()
        err = r.get("ErrorMessage", None)

        if err != None:
            raise Exception(err)


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
                        quantity=abs(int(tds[2].text)),
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
            sgn = 1 if quantity >= 0 else -1
                
            holdings.append(
                Holding(
                    symbol=tds[0].text,
                    quantity=abs(quantity),
                    holding_type=(HoldingType.LONG if quantity >= 0 else HoldingType.SHORT),
                    cost_basis=((float(tds[2].text.replace("$","").replace(",", "")) * quantity) * sgn), 
                    market_value=(float(tds[4].text.replace("$","").replace(",", "")))
                )
            )
        
        return holdings