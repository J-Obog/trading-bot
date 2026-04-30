from datetime import datetime
from typing import List
import requests
from dateutil.parser import parse
from bs4 import BeautifulSoup
import json
from src.yahoo.models import Rating, Sentiment, Split, Tick

BASE_API_URI = "https://query1.finance.yahoo.com/v2/ratings/"
BASE_URI = "https://query2.finance.yahoo.com/v8/finance/chart"
SPLIT_API_URI = "https://query1.finance.yahoo.com/v8/finance/chart"

SPLIT_API_PARAMS = {
    "events": "capitalGain%7Cdiv%7Csplit",
    "formatted": "true",
    "includeAdjustedClose": "true",
    "interval": "1wk",
    "period1": "0",
    "userYfid": "true",
    "lang": "en-US",
    "region": "US"
}


HEADERS = {
    "User-Agent": "StockAnalysis/1.0",
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate, br"
}

STANDARD_QUERY_PARAMS = {
    "includePrePost":"true",
    "events":"div%7Csplit%7Cearn",
    "lang":"en-US",
    "region":"US"
}


BASE_QUERY_PARAMS = {
    "limit": 100,
    "offset": 0,
    "order_by": "fin_score",
    "desc": "true",
    "exclude_noncurrent": "false",
    "lang": "en-US",
    "region": "US"
}

class YahooApi:
    def __init__(self):
        pass

    def get_splits(self, ticker: str) -> List[Split]:
        params = SPLIT_API_PARAMS.copy() | {
            "symbol": ticker,
            "period2": int(datetime.now().timestamp())
        }

        api_url = f"{SPLIT_API_URI}/{ticker}"

        res = requests.get(api_url, headers=HEADERS, params=params).json()

        split_map = res["chart"]["result"][0]["events"].get("splits", [])
        splits = [] 

        for split_date in split_map:
            split = split_map[split_date]

            splits.append(
                Split(
                    date=datetime.fromtimestamp(int(split_date)),
                    effective_date=datetime.fromtimestamp(split["date"]),
                    factor=split["numerator"]/split["denominator"]
                )
            )

        return splits

    def get_ticks(self, ticker: str, t1: datetime, t2: datetime) -> List[Tick]:
        query_params = STANDARD_QUERY_PARAMS
        query_params["period1"] = int(t1.timestamp())
        query_params["period2"] = int(t2.timestamp())
        query_params["interval"] = "1d"
        
        res = requests.get(f"{BASE_URI}/{ticker}", headers=HEADERS, params=query_params)
        data = res.json()["chart"]["result"][0]
        indicators = data["indicators"]["quote"][0]

        timestamps = data["timestamp"]
        closes = indicators["close"]
        opens = indicators["open"]
        highs = indicators["high"]
        lows = indicators["low"]

        ticks: List[Tick] = []

        for i in range(len(timestamps)):
            tick = Tick(
                    timestamp= datetime.fromtimestamp(timestamps[i]),
                    close=closes[i],
                    open=opens[i],
                    lo=lows[i], 
                    hi=highs[i]
                )

            ticks.append(tick)

        return ticks
    


    def get_ratings_v2(self, ticker: str) -> List[Rating]:
        headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/147.0.0.0 Safari/537.36"}
        res = requests.get(f"https://finance.yahoo.com/quote/{ticker.capitalize()}/analyst-insights/", headers=headers)
        
        if res.status_code != 200:
            raise Exception(res.content)
        
        html_text = res.content
        soup = BeautifulSoup(html_text, "html.parser")

        target_script = None

        for script in soup.find_all("script", attrs={"type": "application/json"}):
            data_url = script.get("data-url", "")
            
            if "query1.finance.yahoo.com/v10/finance/quoteSummary" in data_url:
                target_script = script
                break

        if not target_script:
            #raise Exception(f"Target script tag not found for {ticker}")
            print(f"Target script tag not found for {ticker}")
            return []

        outer_json = json.loads(target_script.string.strip())
        inner_json = json.loads(outer_json["body"])
        history = inner_json["quoteSummary"]["result"][0].get("upgradeDowngradeHistory", {}).get("history", [])

        ratings = [] 

        rating_map = {
            "Outperform": Sentiment.BUY,
            "Buy": Sentiment.BUY,
            "Neutral": Sentiment.NEUTRAL,
            "Sector Outperform": Sentiment.BUY,
            "Overweight": Sentiment.BUY,
            "Strong Buy": Sentiment.BUY,
            "Equal-Weight": Sentiment.NEUTRAL,
            "Equal-weight": Sentiment.NEUTRAL,
            "Positive": Sentiment.BUY,
            "Market Outperform": Sentiment.BUY,
            "Hold": Sentiment.NEUTRAL,
            "Market Perform": Sentiment.NEUTRAL,
            "Perform": Sentiment.NEUTRAL,
            "": Sentiment.UKNOWN,
            "Sell": Sentiment.SELL,
            "Long-Term Buy": Sentiment.BUY,
            "Accumulate": Sentiment.BUY,
            "Reduce": Sentiment.SELL,
            "Underperform": Sentiment.SELL,
            "Sector Weight": Sentiment.NEUTRAL,
            "Underweight": Sentiment.SELL,
            "Peer Perform": Sentiment.NEUTRAL,
            "Sector Perform": Sentiment.NEUTRAL,
            "In-Line": Sentiment.NEUTRAL,
            "Top Pick": Sentiment.BUY,
            "Conviction Buy": Sentiment.BUY,
            "In-line": Sentiment.NEUTRAL,
            "Outperformer": Sentiment.BUY,
            "Mixed": Sentiment.NEUTRAL,
            "Market Underperform": Sentiment.SELL,
            "Sector Underperform": Sentiment.SELL,
            "Fair Value": Sentiment.NEUTRAL,
            "Hold Neutral": Sentiment.NEUTRAL,
            "Negative": Sentiment.SELL,
            "Average": Sentiment.NEUTRAL,
            "Market Weight": Sentiment.NEUTRAL,
            "Cautious": Sentiment.NEUTRAL,
            "Strong Sell": Sentiment.SELL,
            "Peer perform": Sentiment.NEUTRAL,
            "Action List Buy": Sentiment.BUY,
            "Add": Sentiment.BUY,
            "Sector Performer": Sentiment.NEUTRAL,
            "Performer": Sentiment.BUY,
            "Underperformer": Sentiment.SELL,
            "Gradually Accumulate": Sentiment.BUY,
            "buy": Sentiment.BUY,
            "Above Average": Sentiment.BUY
        }

        for data in history:
            if data["toGrade"] not in rating_map:
                print(data["toGrade"])

            ratings.append(
                Rating(
                    sentiment= rating_map.get(data["toGrade"], Sentiment.UKNOWN),
                    price_target=data["currentPriceTarget"],
                    uuid="",
                    analyst=data["firm"],
                    announcement_date=datetime.fromtimestamp(data["epochGradeDate"]))
            )

        return ratings


    def get_ratings(self, ticker: str) -> List[Rating]:
        params = BASE_QUERY_PARAMS.copy()
        params["symbol"] = ticker.upper()
        ratings = []
        
        res = requests.get(BASE_API_URI, params=params, headers=HEADERS).json()

        for item in res["items"]:
            raw_sentiment = item["rating_sentiment"] if ("rating_sentiment" in item) and (item["rating_sentiment"] is not None) else None
            ratings.append(
                Rating(
                    sentiment= Sentiment(raw_sentiment) if raw_sentiment is not None else Sentiment.UKNOWN,
                    price_target=item["pt_current"],
                    uuid=item["uuid"],
                    analyst=item["analyst"],
                    announcement_date=parse(item["announcement_date"], ignoretz=True) if item["announcement_date"] is not None else None
                )
            )

        return ratings

