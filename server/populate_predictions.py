from typing import Dict, List
from src.yahoo.models import Sentiment
from src.db.models import Analyst, Prediction
from src.yahoo.api import YahooApi
from pymongo.errors import BulkWriteError
import json
import dotenv
import os
import time
import random
import concurrent.futures
import threading
import src.db.conn
from src.db.models import Sentiment as DbSentiment

dotenv.load_dotenv()

with open("tickers.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

tickers = sorted(data, key=lambda x: x["Market Cap"], reverse=True)[:1000]
db = src.db.conn.get_db(os.environ.get("DB_CONN_URI"))

analyst_cache: Dict[str, Analyst] = {}
prediction_ukey_cache = set()

cache_lock = threading.Lock()


def insert_batch(batch: List[Prediction]):
    if not batch:
        return

    try:
        db.predictions.insert_many(batch, ordered=False)
    except BulkWriteError as err:
        is_legit_err = any(
            x["code"] != 11000 for x in err.details["writeErrors"]
        )
        if is_legit_err:
            raise err


def process_ticker(ticker):
    yahoo = YahooApi()
    ticker_symbol = ticker["Symbol"]
    predictions_to_insert = []

    time.sleep(random.uniform(0.25, 1.15))

    existing_predictions = db.predictions.find({"ticker": ticker_symbol})
    existing_ukeys = {
        f"{p['analyst_id']}:{p['date']}"
        for p in existing_predictions
    }

    with cache_lock:
        prediction_ukey_cache.update(existing_ukeys)

    ratings = yahoo.get_ratings_v2(ticker_symbol)
    ratings = list(
        filter(
            lambda r:
                r.announcement_date is not None
                and r.price_target is not None
                and (
                    r.sentiment == Sentiment.BUY
                    or r.sentiment == Sentiment.SELL
                ),
            ratings,
        )
    )

    with cache_lock:
        known_names = list(analyst_cache.keys())

    for analyst_not_in_cache in db.analysts.find(
        {"name": {"$nin": known_names}}
    ):
        with cache_lock:
            analyst_cache[analyst_not_in_cache["name"]] = analyst_not_in_cache

    analysts_not_in_cache = list(
        filter(
            lambda aname: aname not in analyst_cache,
            map(lambda r: r.analyst, ratings),
        )
    )

    if analysts_not_in_cache:
        try:
            db.analysts.insert_many(
                [Analyst(name=name) for name in analysts_not_in_cache],
                ordered=False,
            )
        except BulkWriteError as err:
            is_legit_err = any(
                x["code"] != 11000 for x in err.details["writeErrors"]
            )
            if is_legit_err:
                raise err

        with cache_lock:
            known_names = list(analyst_cache.keys())

        for analyst_not_in_cache in db.analysts.find(
            {"name": {"$nin": known_names}}
        ):
            with cache_lock:
                analyst_cache[analyst_not_in_cache["name"]] = analyst_not_in_cache

    sentiment_map = {
        Sentiment.BUY: DbSentiment.BULLISH,
        Sentiment.SELL: DbSentiment.BEARISH,
    }

    for rating in ratings:
        with cache_lock:
            analyst_id = analyst_cache[rating.analyst]["_id"]

        prediction = Prediction(
            analyst_id=analyst_id,
            ticker=ticker_symbol,
            date=rating.announcement_date,
            price_target=rating.price_target,
            sentiment=sentiment_map[rating.sentiment],
            outcome=None,
        )

        prediction_ukey = f"{prediction['analyst_id']}:{prediction['date']}"

        with cache_lock:
            if prediction_ukey not in prediction_ukey_cache:
                predictions_to_insert.append(prediction)
                prediction_ukey_cache.add(prediction_ukey)

    batch_size = 50
    for i in range(0, len(predictions_to_insert), batch_size):
        insert_batch(predictions_to_insert[i:i + batch_size])


MAX_WORKERS = 8
with concurrent.futures.ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
    futures = []
    time.sleep(2)

    for rank, ticker in enumerate(tickers):
        futures.append(pool.submit(process_ticker, ticker))
        if rank % MAX_WORKERS == 0:
            time.sleep(2)

    for future in concurrent.futures.as_completed(futures):
        future.result()

db.close()