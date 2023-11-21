from typing import Optional
from trading.airtable import AirtableSyncer
from trading.data import Holding, HoldingType, Order, OrderType, StockRatingType, TopCompany
from trading.manager import TradingManager
from trading.nasdaq import NasdaqClient
from trading.street import WallStreetSurvivorClient
import time
import os
import dotenv

dotenv.load_dotenv()


trading_client = WallStreetSurvivorClient(os.getenv("COOKIE"))

syncer = AirtableSyncer(os.getenv("AIRTABLE_ACCESS_TOKEN"), "appXOrXAKdltkZqtu")

syncer.sync_portfolio_tbl(trading_client.get_holdings())

#

#ods = trading_client.get_pending_orders()



