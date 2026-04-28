from typing import List
from src.yahoo.models import Sentiment
from src.db.models import Analyst, Prediction
from src.yahoo.api import YahooApi
import json
import dotenv
import os
import time
import concurrent.futures
import src.db.conn
from src.db.models import Sentiment as DbSentiment

dotenv.load_dotenv()

with open("tickers.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

tickers = sorted(data, key=lambda x: x["Market Cap"], reverse=True)[:2000]

db = src.db.conn.get_db(os.environ.get("DB_CONN_URI"))
yahoo = YahooApi()

predictions_to_insert = []

for ticker in tickers:
    time.sleep(0.005)
    ratings = yahoo.get_ratings(ticker["Symbol"])
    
    for rating in ratings:
        if(rating.announcement_date is None) or (rating.price_target is None) or (rating.sentiment == Sentiment.UKNOWN) or (rating.sentiment == Sentiment.NEUTRAL):
            continue 

        analyst = db.analysts.find_one({"name": rating.analyst})
        analyst_id = analyst["_id"] if analyst is not None else None

        if analyst_id is None:
            analyst_id = db.analysts.insert_one(Analyst(
                name=rating.analyst
            )).inserted_id

        sentiment_map = {
            Sentiment.BUY: DbSentiment.BULLISH,
            Sentiment.SELL: DbSentiment.BEARISH
        }

        prediction = Prediction(
            analyst_id=analyst_id,
            ticker=ticker["Symbol"], 
            date=rating.announcement_date, 
            price_target=rating.price_target,
            sentiment=sentiment_map[rating.sentiment],
            outcome=None
        )

        predictions_to_insert.append(prediction)

def insert_batch(batch: List[Prediction]):
    db.predictions.insert_many(batch)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    batch_size = 100

    for i in range(0, len(predictions_to_insert), batch_size):
        pool.submit(insert_batch, predictions_to_insert[i:i + batch_size])


db.close()