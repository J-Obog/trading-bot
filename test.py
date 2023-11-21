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

ods = trading_client.get_pending_orders()


print(ods)
#nasdaq_client = NasdaqClient()

#manager = TradingManager(trading_client, nasdaq_client)


