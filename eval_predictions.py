from datetime import datetime
from airtable import AirtableApi, Outcome, OutcomeUpdate
from yahoo import YahooApi
import dotenv
import os

dotenv.load_dotenv()

airtable = AirtableApi(
    os.environ.get("AIRTABLE_TOKEN"), 
    os.environ.get("AIRTABLE_BASE_ID"), 
    os.environ.get("AIRTABLE_TABLE_ID")
)

yahoo = YahooApi()

predictions = sorted(airtable.get_all_predictions(),key=lambda x: x.announcement_date,)

unique_tickers = set(map(lambda x: x.ticker, predictions))

outcome_updates = []

for ticker in unique_tickers:
    predictions_for_ticker = list(filter(lambda x: (x.ticker == ticker) and (x.outcome is None), predictions))
    if len(predictions_for_ticker) == 0:
        continue
    
    chart_ticks = yahoo.get_ticks(ticker, predictions_for_ticker[0].announcement_date, predictions_for_ticker[-1].expiration_date)

    for ticker_prediction in predictions_for_ticker:
        close_date = None
        for t in chart_ticks:
            if (t.hi is None) or (t.timestamp is None):
                #print(ticker)
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

airtable.update_prediction_outcomes(outcome_updates)