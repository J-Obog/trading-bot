import os
from typing import List, Optional
from bs4 import BeautifulSoup
import dotenv
import requests
from trading.data import Holding, HoldingType, Order, OrderType, StockRatingType
from trading.nasdaq import NasdaqClient
from trading.wallstreet import WallStreetSurvivorClient

DEFAULT_QUANTITY = 5

def get_top_companies() -> List[str]:
    comapnies = [] 

    html_content = requests.get("https://stockanalysis.com/list/biggest-companies/").content
    sp = BeautifulSoup(html_content, "html.parser")
    tbl = sp.find(id="main-table")
    tbody = tbl.find("tbody")

    for tr in tbody.find_all("tr"):
        tds = tr.find_all("td")        
        comapnies.append(tds[1].text)
    
    return comapnies

def get_trade_action(rating: StockRatingType, current_holding: Optional[Holding]) -> Optional[OrderType]:
    if rating == StockRatingType.HOLD:
        return None
        
    if current_holding == None:
        return OrderType.BUY if rating == StockRatingType.BUY else OrderType.SHORT
    else:
        holding_type = current_holding.holding_type

        if (holding_type == HoldingType.LONG) and (rating == StockRatingType.SELL):
            return OrderType.SELL
        
        if (holding_type == HoldingType.SHORT) and (rating == StockRatingType.BUY):
            return OrderType.BUY_TO_COVER

        return None
    
dotenv.load_dotenv()

portfolio_client = WallStreetSurvivorClient(os.getenv("COOKIE"))
stock_client = NasdaqClient()


holdings = portfolio_client.get_holdings()
holdings_map = {holding.symbol: holding for holding in holdings}

top_companies = get_top_companies()[:10]

for ticker in top_companies:
    if ticker not in holdings_map:
        holdings_map[ticker] = None

pending_orders = portfolio_client.get_pending_orders()

for symbol, holding in holdings_map.items():
    rating = stock_client.get_rating(symbol)

    if rating == StockRatingType.NONE:
        continue
    
    order_type = None

    if rating != StockRatingType.HOLD:
        if holding == None:
            order_type = OrderType.BUY if rating == StockRatingType.BUY else OrderType.SHORT
        else:
            holding_type = holding.holding_type

            if (holding_type == HoldingType.LONG) and (rating == StockRatingType.SELL):
                order_type = OrderType.SELL
            
            if (holding_type == HoldingType.SHORT) and (rating == StockRatingType.BUY):
                order_type = OrderType.BUY_TO_COVER
                
    if order_type != None:
        print(f"Preparing to execute {order_type} order for {symbol}")

    if order_type != None:
        quantity = DEFAULT_QUANTITY if holding == None else holding.quantity
        
        order = Order(quantity, symbol, order_type)
        has_already_been_placed = False

        for pending_order in pending_orders:
            if (order.symbol == pending_order.symbol) and (order.order_type == pending_order.order_type):
                has_already_been_placed = True
                break

        if not(has_already_been_placed):
            portfolio_client.place_order(order)
        else:
            print(f"not placing order for {symbol} since there is an existing one")