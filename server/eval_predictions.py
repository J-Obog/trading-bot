from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import time
from dateutil.relativedelta import relativedelta
from typing import Dict, List

from pymongo import UpdateOne
from src.yahoo.models import Split, Tick
from src.db.models import Outcome, Prediction, Sentiment
from src.yahoo.api import YahooApi
import src.db.conn
import dotenv
import os

dotenv.load_dotenv()

db = src.db.conn.get_db(os.environ.get("DB_CONN_URI"))
yahoo = YahooApi()

ticker_to_prediction_map: Dict[str, List[Prediction]] = {}

for prediction in db.predictions.find({"outcome": {"$eq": None}}):
    if prediction["ticker"] not in ticker_to_prediction_map:
        ticker_to_prediction_map[prediction["ticker"]] = []

    ticker_to_prediction_map[prediction["ticker"]].append(prediction)

current_datetime = datetime.now()

def adjust_for_splits(splits: List[Split], ticks: List[Tick]) -> List[Tick]:
    adj_ticks = []
    split_ranges = []
    
    sorted_splits = sorted(splits, key=lambda s: s.effective_date)
    
    for split in sorted_splits:
        lb = split_ranges[-1]["ub"] if len(split_ranges) > 0 else datetime(1,1,1)
        ub = split.date
        cm = split.factor
        for i in range(len(split_ranges)):
            split_ranges[i]["cm"] *= cm

        split_ranges.append({"lb": lb, "ub": ub, "cm": cm})

    split_ranges.append({"lb": split_ranges[-1]["ub"], "ub": datetime(2099, 1, 1), "cm": 1})

    for tick in ticks:
        tick_date = datetime.fromtimestamp(tick.timestamp)
        found_split_ranges = list(filter(lambda sr: sr["lb"] <= tick_date < sr["ub"], split_ranges))
        
        if found_split_ranges != 1:
            raise "Found ranges size is not exactly one" 

        cum_mult = found_split_ranges[0]["cm"]
        
        adj_ticks.append(
            Tick(
                hi=tick.hi*cum_mult,
                lo=tick.lo*cum_mult,
                open=tick.open*cum_mult,
                close=tick.close*cum_mult,
                timestamp=tick.timestamp
            )
        )

    return adj_ticks

def process_ticker(ticker: str):
    sorted_predictions = sorted(
        ticker_to_prediction_map[ticker],
        key=lambda p: p["date"]
    )

    splits = yahoo.get_splits(ticker)

    chart_ticks = yahoo.get_ticks(
        ticker,
        sorted_predictions[0]["date"],
        sorted_predictions[-1]["date"] + relativedelta(years=1)
    )

    if len(splits) > 0:
        chart_ticks = adjust_for_splits(splits, chart_ticks)

    updates = []


    for ticker_prediction in sorted_predictions:
        horizon = ticker_prediction["date"] + relativedelta(years=1)
        price_target = ticker_prediction["price_target"]

        tick_hits_target_fn = (
            lambda t: t.hi >= price_target
            if ticker_prediction["sentiment"] == Sentiment.BULLISH
            else t.lo <= price_target
        )

        filtered_ticks = filter(
            lambda t: None not in [t.hi, t.lo, t.timestamp],
            chart_ticks
        )
        filtered_ticks = filter(
            lambda t: ticker_prediction["date"] < t.timestamp <= horizon,
            filtered_ticks
        )
        filtered_ticks = filter(
            tick_hits_target_fn,
            filtered_ticks
        )

        is_correct = len(list(filtered_ticks)) > 0
        update_query = {"_id": ticker_prediction["_id"]}

        if is_correct:
            updates.append(
                UpdateOne(
                    filter=update_query,
                    update={"$set": {"outcome": Outcome.CORRECT}}
                )
            )
        elif current_datetime > horizon:
            updates.append(
                UpdateOne(
                    filter=update_query,
                    update={"$set": {"outcome": Outcome.WRONG}}
                )
            )

    if updates:
        db.predictions.bulk_write(updates)

    return ticker, len(updates)

MAX_POOL_SIZE = 8
with ThreadPoolExecutor(max_workers=MAX_POOL_SIZE) as executor:
    futures = []

    for i, ticker in enumerate(ticker_to_prediction_map):
        if ticker == "TSLA":
            futures.append(executor.submit(process_ticker, ticker))

            if i % MAX_POOL_SIZE == 0:
                time.sleep(0.25)

    for future in as_completed(futures):
        ticker, updated_count = future.result()
        print(
            f"Finished with updates for ticker {ticker}, "
            f"updated {updated_count} rows"
        )


db.close()