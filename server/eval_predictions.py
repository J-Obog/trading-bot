from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Dict, List
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

for ticker in ticker_to_prediction_map:    
    sorted_predictions = sorted(ticker_to_prediction_map[ticker], key=lambda p: p["date"])
    chart_ticks = yahoo.get_ticks(ticker, sorted_predictions[0]["date"], sorted_predictions[-1]["date"] + relativedelta(years=1))

    for ticker_prediction in sorted_predictions:
        horizon = ticker_prediction["date"] + relativedelta(years=1)
        price_target = ticker_prediction["price_target"]
        tick_hits_target_fn = lambda t: t.hi >= price_target if ticker_prediction["sentiment"] == Sentiment.BULLISH else t.lo <= price_target
          
        filtered_ticks = filter(lambda t: None not in [t.hi, t.lo, t.timestamp], chart_ticks)
        filtered_ticks = filter(lambda t: ticker_prediction["date"] < t.timestamp <= horizon, filtered_ticks)
        is_correct = any(tick_hits_target_fn, filtered_ticks)

        update_query = {"_id": ticker_prediction["_id"]}

        if is_correct:
            db.predictions.update_one(update_query, {"outcome": Outcome.CORRECT})
        else:
            if current_datetime > horizon:
                db.predictions.update_one(update_query, {"outcome": Outcome.WRONG})

db.close()