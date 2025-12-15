from yahoo import YahooApi
import json


top_sp500_tickers = []

with open("top_sp500.json", "r", encoding="utf-8") as json_file:
    top_sp500_tickers = json.load(json_file)

analysis = YahooApi()


for ticker in top_sp500_tickers:
    ratings = analysis.get_ratings(ticker)



