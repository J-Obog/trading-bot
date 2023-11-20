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

trading_client.make_order(Order(10, "GME", OrderType.BUY))