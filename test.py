from typing import Optional
from trading.data import Holding, HoldingType, Order, OrderType, StockRatingType, TopCompany
from trading.investopedia import InvestopediaClient
from trading.nasdaq import NasdaqClient
import time
import dotenv
import os
from trading.street import WallStreetSurvivorClient

def get_order(rating_type: StockRatingType, holding: Optional[Holding]) -> Optional[OrderType]:
    if rating_type != StockRatingType.HOLD:
        signal = "buy" if ((rating_type == StockRatingType.BUY) or (rating_type == StockRatingType.STRONG_BUY)) else "sell"

        if holding == None:
            return OrderType.BUY if signal == "buy" else OrderType.SHORT
        else:
            holding_type = holding.holding_type

            if holding_type == HoldingType.LONG and signal == "sell":
                return OrderType.SELL
            
            if holding_type == HoldingType.SHORT and signal == "buy":
                return OrderType.BUY_TO_COVER
        
            # TODO: this may need to be updated to support buying more shares or shorting more shares
            return None
    
    return None


dotenv.load_dotenv()

trading_client = WallStreetSurvivorClient(os.getenv("COOKIE"))
nasdaq_client = NasdaqClient()

#top_mkt_cap_companies = nasdaq_client.get_top_companies()[:5]
top_mkt_cap_companies = [TopCompany("SNAP"), TopCompany("GOOGL")]


holdings = trading_client.get_holdings()
holdings_map = {holding.symbol: holding for holding in holdings}

for company in top_mkt_cap_companies:    
    symbol = company.symbol.upper()
    stock_rating = nasdaq_client.get_rating(symbol)

    holding = holdings_map.get(symbol, None)

    order_to_execute = get_order(stock_rating.rating, holding)

    if order_to_execute is not None:
        trading_client.place_trade(Order(10, symbol, order_to_execute))

    print()
    print(symbol, stock_rating, order_to_execute, holding)

