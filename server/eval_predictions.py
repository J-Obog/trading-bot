from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from typing import Dict, List
from server.src.db.models import Prediction
from src.yahoo.api import YahooApi
import src.db.conn
import dotenv
import os
import concurrent.futures

dotenv.load_dotenv()

db = src.db.conn.get_db(os.environ.get("DB_CONN_URI"))
yahoo = YahooApi()


ticker_to_prediction_map: Dict[str, List[Prediction]] = {}

for prediction in db.predictions.find({"outcome": {"$ne": None}}):
    if prediction["ticker"] not in ticker_to_prediction_map:
        ticker_to_prediction_map[prediction["ticker"]] = []

    ticker_to_prediction_map[prediction["ticker"]].append(prediction)

for ticker in ticker_to_prediction_map:
    sorted_predictions = sorted(ticker_to_prediction_map[ticker], key=lambda p: p["date"])
    chart_ticks = yahoo.get_ticks(ticker, sorted_predictions[0]["date"], sorted_predictions[-1]["date"] + relativedelta(years=1))

    for ticker_prediction in predictions_for_ticker:
        close_date = None
        for t in chart_ticks:
            if (t.hi is None) or (t.timestamp is None):
                continue
            if (t.timestamp >= ticker_prediction.announcement_date) and (t.timestamp < ticker_prediction.expiration_date) and (t.hi >= ticker_prediction.price_target):
                close_date = t.timestamp
                break

        if close_date is not None:
            outcome_updates.append(OutcomeUpdate(ticker_prediction.record_id, close_date, Outcome.RIGHT))
        else:
            time_now = datetime.now()
            if time_now >= ticker_prediction.expiration_date:
                outcome_updates.append(OutcomeUpdate(ticker_prediction.record_id, ticker_prediction.expiration_date, Outcome.WRONG))


def insert_batch(batch: List[OutcomeUpdate]):
    airtable.update_prediction_outcomes(batch)

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    batch_size = 100

    for i in range(0, len(outcome_updates), batch_size):
        pool.submit(insert_batch, outcome_updates[i:i + batch_size])
        