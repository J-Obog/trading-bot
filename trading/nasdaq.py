from typing import List, Optional
from bs4 import BeautifulSoup
import requests
from trading.data import StockRating, StockRatingType, TopCompany

ANALYST_API_URL = "https://api.nasdaq.com/api/analyst"
URL = "https://stockanalysis.com/list/biggest-companies/"

class NasdaqClient:
    def __init__(self):
        self.sess = requests.Session()

    def get_rating(self, symbol: str) -> Optional[StockRating]:
        data = self.sess.get(f"{ANALYST_API_URL}/{symbol}/ratings").json()["data"]
        
        return StockRating(
            rating=StockRatingType(data["meanRatingType"]),
            rating_entities=set()
        )
    
    def get_top_companies(self) -> List[TopCompany]:
        comapnies = [] 

        html_content = requests.get(URL).content
        sp = BeautifulSoup(html_content, "html.parser")
        tbl = sp.find(id="main-table")
        tbody = tbl.find("tbody")

        for tr in tbody.find_all("tr"):
            tds = tr.find_all("td")        
            comapnies.append(
                TopCompany(
                    symbol=tds[1].text
                )
            )
        
        return comapnies