from datetime import timedelta, timezone
from typing import List
from airtable import AirtableApi, Prediction
from yahoo import Sentiment, YahooApi
import json
import dotenv
import os
import time
import concurrent.futures

dotenv.load_dotenv()

data = []

def get_unique_key(prediction: Prediction) -> str:
    return f'{prediction.ticker}:{prediction.analyst}:{prediction.announcement_date.strftime("%m/%d/%Y")}'

with open("tickers.json", "r", encoding="utf-8") as json_file:
    data = json.load(json_file)

airtable = AirtableApi(
    os.environ.get("AIRTABLE_TOKEN"), 
    os.environ.get("AIRTABLE_BASE_ID"), 
    os.environ.get("AIRTABLE_TABLE_ID")
)

yahoo = YahooApi()

existing_ids = set(map(lambda x: get_unique_key(x), airtable.get_all_predictions()))

new_predictions = []

for datum in sorted(data, key=lambda x: x["Market Cap"], reverse=True)[:500]:
    time.sleep(0.005)
    ratings = yahoo.get_ratings(datum["Symbol"])

    for rating in ratings:
        if (rating.price_target is None) or (rating.sentiment != Sentiment.BUY):
            continue

        p = Prediction(
            id=rating.uuid, 
            ticker=datum["Symbol"], 
            analyst=rating.analyst, 
            announcement_date=rating.announcement_date, 
            price_target=rating.price_target, 
            outcome=None, 
            close_date=None, 
            expiration_date = rating.announcement_date + timedelta(days=180)
        )

        ukey = get_unique_key(p)

        if ukey in existing_ids:
            continue

        new_predictions.append(p)
        existing_ids.add(ukey)


def insert_batch(batch: List[Prediction]):
    airtable.create_predictions(batch)

with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    batch_size = 100

    for i in range(0, len(new_predictions), batch_size):
        pool.submit(insert_batch, new_predictions[i:i + batch_size])

