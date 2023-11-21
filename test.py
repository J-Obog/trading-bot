from typing import Optional
from trading.data import Holding, HoldingType, Order, OrderType, StockRatingType
from trading.investopedia import InvestopediaClient
from trading.nasdaq import NasdaqClient
import time
import dotenv
import os

from trading.street import WallStreetSurvivorClient

dotenv.load_dotenv()

trading_client = WallStreetSurvivorClient(os.getenv("COOKIE"))


print(trading_client.get_holdings())
#r = trading_client.place_trade(Order(10, "GME", OrderType.BUY))
#print(r)

