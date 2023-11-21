from typing import List, Optional
from bs4 import BeautifulSoup
import requests
from trading.data import StockRating, StockRatingType, TopCompany

ANALYST_API_URL = "https://api.nasdaq.com/api/analyst"
URL = "https://stockanalysis.com/list/biggest-companies/"

class NasdaqClient:
    def __init__(self):
        self.sess = requests.Session()
        self.sess.headers["User-Agent"] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'

    def get_rating(self, symbol: str) -> Optional[StockRating]:
        data = self.sess.get(ANALYST_API_URL + "/" + symbol +  "/ratings").json()["data"]
        
        return StockRating(
            rating=StockRatingType.from_nasdaq_type(data["meanRatingType"]),
            rating_entities=set()
        )
    
    def get_top_companies(self) -> List[TopCompany]:
        companies = [] 

        html_content = requests.get(URL).content
        sp = BeautifulSoup(html_content, "html.parser")
        tbl = sp.find(id="main-table")
        tbody = tbl.find("tbody")

        for tr in tbody.find_all("tr"):
            tds = tr.find_all("td")        
            companies.append(
                TopCompany(
                    symbol=tds[1].text
                )
            )
        
        return companies