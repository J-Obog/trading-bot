from datetime import timedelta
from airtable import AirtableApi, Prediction
from yahoo import Sentiment, YahooApi
import json
import dotenv
import os
import time

dotenv.load_dotenv()

top_tickers = []

def get_unique_key(prediction: Prediction) -> str:
    return f'{prediction.analyst}:{prediction.announcement_date.strftime("%m/%d/%Y")}'

with open("top_sp500.json", "r", encoding="utf-8") as json_file:
    top_tickers = json.load(json_file)

airtable = AirtableApi(
    os.environ.get("AIRTABLE_TOKEN"), 
    os.environ.get("AIRTABLE_BASE_ID"), 
    os.environ.get("AIRTABLE_TABLE_ID")
)

yahoo = YahooApi()

existing_ids = set(map(lambda x: get_unique_key(x), airtable.get_all_predictions()))

new_predictions = []

for ticker in top_tickers:
    time.sleep(0.5)
    ratings = yahoo.get_ratings(ticker)

    for rating in ratings:
        if (rating.uuid in existing_ids) or (rating.price_target is None) or (rating.sentiment != Sentiment.BUY):
            continue

        p = Prediction(
            id=rating.uuid, 
            ticker=ticker, 
            analyst=rating.analyst, 
            announcement_date=rating.announcement_date, 
            price_target=rating.price_target, 
            outcome=None, 
            close_date=None, 
            expiration_date = rating.announcement_date + timedelta(days=180)
        )

        new_predictions.append(p)
        existing_ids.add(get_unique_key(p))

airtable.create_predictions(new_predictions)

