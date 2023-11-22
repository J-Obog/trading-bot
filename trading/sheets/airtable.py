from typing import Dict, List
from pyairtable import Api, Table

from trading.data import Holding, HoldingType


BASE_ID = "appXOrXAKdltkZqtu"
PORTFOLIO_TABLE_ID = "tblcTLEbUaloK69TV"


def delete_all(tbl: Table):
    recs = tbl.all()
    tbl.batch_delete([rec["id"] for rec in recs])

def create_all(tbl: Table, recs: List[Dict]):
    tbl.batch_create(recs)

class AirtableClient:
    def __init__(self, token: str):
        api = Api(token)
        self.portfolio_tbl = api.table(BASE_ID, PORTFOLIO_TABLE_ID)

    def build_holdings_sheet(self, holdings: List[Holding]):
        delete_all(self.portfolio_tbl)
        
        recs = []
        
        for holding in holdings:
            ticker = holding.symbol.upper()

            logo_url = f"https://neutrongroup.cachefly.net/logos/{ticker}.gif"
            logo_url = f"https://eodhd.com/img/logos/US/{ticker}.png"
            pl = (holding.market_value - holding.cost_basis) if holding.holding_type == HoldingType.LONG else (holding.cost_basis - holding.market_value) 

            recs.append({
                "Ticker": ticker, 
                "Logo": [{"url": logo_url}], 
                "Quantity": str(holding.quantity),
                "Cost Basis": holding.cost_basis,
                "Market Value": holding.market_value,
                "P/L": pl
            })

        create_all(self.portfolio_tbl, recs)