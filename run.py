from trading.data import StockRatingType
from trading.investopedia import InvestopediaClient
from trading.nasdaq import NasdaqClient
import time

trading_client = InvestopediaClient()
nasdaq_client = NasdaqClient()

top_mkt_cap_companies = nasdaq_client.get_top_companies()

while True:
    holdings = trading_client.get_holdings()
    holdings_map = {holding.symbol: holding for holding in holdings}

    for company in top_mkt_cap_companies:
        symbol = company.symbol.upper()
        stock_rating = nasdaq_client.get_rating(symbol)
        rating_type = stock_rating.rating

        if rating_type == StockRatingType.HOLD:
            continue
        
        signal = "buy" if ((rating_type == StockRatingType.BUY) or (rating_type == StockRatingType.SELL)) else "sell"

        holding = holdings_map.get(symbol, None)

        if holding is None:
            pass
        else:
            pass

        time.sleep(60 * 1)

    time.sleep(60 * 15)
