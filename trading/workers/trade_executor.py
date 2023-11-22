from typing import List, Optional
from trading.data import Holding, HoldingType, Order, OrderType, StockRatingType
from trading.nasdaq import NasdaqClient
from trading.portfolio.client import PortfolioClient
from trading.stocks.client import StockClient
from trading.trading import TradingClient
from trading.workers.worker import Worker


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
        
     
class TradeExecutorWorker(Worker):
    def __init__(self, 
                 portfolio_client: PortfolioClient, 
                 stock_client: StockClient
        ):

        self.portfolio_client = portfolio_client
        self.stock_client = stock_client

    def run(self):
        symbols = [] 

        holdings = self.portfolio_client.get_holdings()
        holdings_map = {holding.symbol: holding for holding in holdings}
        pending_orders = self.portfolio_client.get_pending_orders()

        for symbol in symbols:
            rating = self.stock_client.get_rating(symbol)
            holding = holdings_map.get(symbol, None)

            order_type = get_trade_action(rating, holding)

            if order_type != None:
                order = Order(10, symbol, order_type)
                has_already_been_placed = False
            
                for pending_order in pending_orders:
                    if order == pending_order:
                        has_already_been_placed = True
                        break
            
                if not(has_already_been_placed):
                    self.portfolio_client.place_order(order)


        

