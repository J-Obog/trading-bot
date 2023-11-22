import time
import os
from typing import List
import dotenv
from trading.portfolio.wall_street import WallStreetSurvivorClient
from trading.stocks.nasdaq import NasdaqClient
from trading.workers.trade_executor import TradeExecutorWorker
from trading.workers.worker import Worker

dotenv.load_dotenv()

RUN_CADENCE = 60 * 5
BETWEEN_EXEC_CADENCE = 5
MAX_ITRS = 1

itrs = 0 


portfolio_client = WallStreetSurvivorClient(os.getenv("COOKIE"))
stock_client = NasdaqClient()

trade_executor = TradeExecutorWorker(portfolio_client, stock_client)

while True:
    workers: List[Worker] = [trade_executor]

    for worker in workers:
        worker.run()
        time.sleep(BETWEEN_EXEC_CADENCE)
    
    itrs += 1

    if (MAX_ITRS != None) and (itrs == MAX_ITRS):
        break

    time.sleep(RUN_CADENCE)