from typing import List
from src.db.models import Analyst, Prediction
from src.yahoo.api import YahooApi
import json
import dotenv
import os
import time
import concurrent.futures
import src.db.conn

dotenv.load_dotenv()

with open("tickers.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

tickers = sorted(data, key=lambda x: x["Market Cap"], reverse=True)[:1]

db = src.db.conn.get_db(os.environ.get("DB_CONN_URI"))
yahoo = YahooApi()

predictions_to_insert = []

for ticker in tickers:
    time.sleep(0.005)
    ratings = yahoo.get_ratings(ticker["Symbol"])

    for rating in ratings:
        if (rating.price_target is None):
            print("Rating is not present")
            continue


        analyst = db.analysts.find_one({"name": rating.analyst})
        analyst_id = analyst["_id"] if analyst is not None else None

        if analyst_id is None:
            print(f"Couldn't find analyst {rating.analyst} in db, creating new analyst record")
            analyst_id = db.analysts.insert_one(Analyst(
                name=rating.analyst
            )).inserted_id

        prediction = Prediction(
            analyst_id=analyst_id,
            ticker=ticker["Symbol"], 
            date=rating.announcement_date, 
            price_target=rating.price_target
        )

        predictions_to_insert.append(prediction)

def insert_batch(batch: List[Prediction]):
    db.predictions.insert_many(batch)

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    batch_size = 100

    for i in range(0, len(predictions_to_insert), batch_size):
        pool.submit(insert_batch, predictions_to_insert[i:i + batch_size])
