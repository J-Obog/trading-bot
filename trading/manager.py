

from typing import List, Optional
from trading.data import Holding, HoldingType, Order, OrderType, StockRatingType
from trading.nasdaq import NasdaqClient
from trading.street import WallStreetSurvivorClient


class TradingManager:
    def __init__(self, trading_client: WallStreetSurvivorClient, analysis_client: NasdaqClient):
        self.trading_client = trading_client
        self.analysis_client = analysis_client

    # TODO: this may need to be updated to support buying more shares or shorting more shares
    def get_orders_to_make(self, symbols: List[str]) -> List[Order]:
        orders = []
        
        holdings = self.trading_client.get_holdings()
        holdings_map = {holding.symbol: holding for holding in holdings}

        for symbol in symbols:
            rating = self.analysis_client.get_rating(symbol).rating
            holding = holdings_map.get(symbol, None)

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
                orders.append(Order(10, symbol, order_type))

        return orders     
                     
    def process_orders(self, orders: List[Order]):
        pending_orders = self.trading_client.get_pending_orders()
        
        for order in orders:
            has_already_been_placed = False
            
            for pending_order in pending_orders:
                if order == pending_order:
                    has_already_been_placed = True
                    break
            
            if not(has_already_been_placed):
                self.trading_client.place_trade(order)
        

