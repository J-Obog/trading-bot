from datetime import timedelta
from airtable import AirtableApi, Prediction
from yahoo import Sentiment, YahooApi
import json

top_tickers = []

with open("top_sp500.json", "r", encoding="utf-8") as json_file:
    top_tickers = json.load(json_file)

airtable = AirtableApi("", "", "")
yahoo = YahooApi()

existing_ids = set(map(lambda x: x.id, airtable.get_all_predictions()))

new_predictions = []

for ticker in top_tickers:
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
            expiration_date = rating.announcement_date + timedelta(days=365)
        )

        new_predictions.append(p)
        existing_ids.add(rating.uuid)

airtable.create_predictions(new_predictions)

