from typing import Optional
from trading.data import Holding, HoldingType, Order, OrderType, StockRatingType, TopCompany
from trading.manager import TradingManager
from trading.nasdaq import NasdaqClient
from trading.street import WallStreetSurvivorClient
import time
import os
import dotenv

dotenv.load_dotenv()

trading_client = WallStreetSurvivorClient(os.getenv("COOKIE"))
nasdaq_client = NasdaqClient()

manager = TradingManager(trading_client, nasdaq_client)



top_mkt_cap_companies = nasdaq_client.get_top_companies()[:5]

#orders = manager.get_orders_to_make([cmp.symbol for cmp in top_mkt_cap_companies])
orders = manager.get_orders_to_make(["NVDA", "AMZN", "GME", "GOOGL", "META"])



#for ordr in orders:
#    print(ordr)
#    print()
