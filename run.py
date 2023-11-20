from typing import Optional
from trading.data import Holding, HoldingType, Order, OrderType, StockRatingType
from trading.investopedia import InvestopediaClient
from trading.nasdaq import NasdaqClient
import time

trading_client = InvestopediaClient()
nasdaq_client = NasdaqClient()

top_mkt_cap_companies = nasdaq_client.get_top_companies()

def get_order(rating_type: StockRatingType, symbol: str, holding: Optional[Holding]) -> Optional[Order]:
    if rating_type == StockRatingType.HOLD:
        return None
        
    signal = "buy" if ((rating_type == StockRatingType.BUY) or (rating_type == StockRatingType.SELL)) else "sell"

    if holding is None:
        if signal == "buy":
            return trading_client.make_trade(Order(quantity=10, symbol=symbol, order_type=OrderType.BUY))
        else:
            return trading_client.make_trade(Order(quantity=10, symbol=symbol, order_type=OrderType.SHORT))
    
    holding_type = holding.holding_type

    if holding_type == HoldingType.LONG and signal == "sell":
        return trading_client.make_trade(Order(quantity=10, symbol=symbol, order_type=OrderType.SELL))
    
    if holding_type == HoldingType.SHORT and signal == "buy":
        return trading_client.make_trade(Order(quantity=10, symbol=symbol, order_type=OrderType.BUY_TO_COVER))
    
    # TODO: this may need to be updated to support buying more shares or shorting more shares
    return None

while True:
    holdings = trading_client.get_holdings()
    holdings_map = {holding.symbol: holding for holding in holdings}

    for company in top_mkt_cap_companies:
        symbol = company.symbol.upper()
        stock_rating = nasdaq_client.get_rating(symbol)
       
        holding = holdings_map.get(symbol, None)

        order_to_execute = get_order(stock_rating.rating, symbol, holding)

        if order_to_execute is not None:
            trading_client.make_trade(order_to_execute)

        time.sleep(60 * 1)

    time.sleep(60 * 15)
