from typing import Dict, List
from pyairtable import Api, Table

from trading.data import Holding

def delete_all(tbl: Table):
    recs = tbl.all()
    tbl.batch_delete([rec["id"] for rec in recs])

def create_all(tbl: Table, recs: List[Dict]):
    tbl.batch_create(recs)

class AirtableSyncer:
    def __init__(self, token: str, base_id: str):
        api = Api(token)
        self.portfolio_tbl = api.table(base_id, 'tblcTLEbUaloK69TV')

    def sync_portfolio_tbl(self, holdings: List[Holding]):
        delete_all(self.portfolio_tbl)

        recs = []
       
        for holding in holdings:
            ticker = holding.symbol.upper()

            recs.append({
                "Ticker": ticker, 
                "Logo": [{"url": f"https://eodhd.com/img/logos/US/{ticker}.png"}], 
                "Quantity": "10",
                "Position": holding.holding_type.name.lower().capitalize()
            })

        create_all(self.portfolio_tbl, recs)