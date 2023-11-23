import os
from typing import Optional
import dotenv
from trading.data import Holding, HoldingType, Order, OrderType, StockRatingType
from trading.portfolio.wall_street import WallStreetSurvivorClient
from trading.sheets.airtable import AirtableClient
from trading.stocks.nasdaq import NasdaqClient

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
ssheet_client = AirtableClient(os.getenv("AIRTABLE_ACCESS_TOKEN"))
stock_client = NasdaqClient()

symbols = ["AAPL", "META", "GOOGL", "AMZN", "SCCO"] # this has to be updated 

holdings = portfolio_client.get_holdings()
holdings_map = {holding.symbol: holding for holding in holdings}
pending_orders = portfolio_client.get_pending_orders()

for symbol in symbols:
    rating = stock_client.get_rating(symbol)
    current_holding = holdings_map.get(symbol, None)
    order_type = None

    if rating != StockRatingType.HOLD:
        if current_holding == None:
            order_type = OrderType.BUY if rating == StockRatingType.BUY else OrderType.SHORT
        else:
            holding_type = current_holding.holding_type

            if (holding_type == HoldingType.LONG) and (rating == StockRatingType.SELL):
                order_type = OrderType.SELL
            
            if (holding_type == HoldingType.SHORT) and (rating == StockRatingType.BUY):
                order_type = OrderType.BUY_TO_COVER
                
    if order_type != None:
        print(f"Preparing to execute {order_type} order for {symbol}")

    if order_type != None:
        quantity = 10 if current_holding == None else current_holding.quantity
        
        order = Order(quantity, symbol, order_type)
        has_already_been_placed = False

        for pending_order in pending_orders:
            if order == pending_order:
                has_already_been_placed = True
                break

        if not(has_already_been_placed):
            portfolio_client.place_order(order)
        else:
            print(f"not placing order for {symbol} since there is an existing one")