import json
import csv

tickers = set()

def populate_tickers_from_file(filename):
    with open(filename, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)

        for row in csv_reader:
            tickers.add(row["Symbol"])

populate_tickers_from_file("nyse.csv")
populate_tickers_from_file("nasdaq.csv")

with open("tickers.json", "w+", encoding="utf-8") as json_file:
    json.dump(sorted(list(tickers)), json_file)