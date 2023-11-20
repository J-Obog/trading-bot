from typing import List
import requests

from trading.data import Holding, Order

API_URL = "https://api.investopedia.com/simulator/graphql"

class InvestopediaClient:
    def __init__(self):
        self.sess = requests.Session()
        self.portfolio_id = ""

    def make_trade(self, order: Order):
        body = {
            "operationName": "StockTrade",
            "variables": {
                "input": {
                    "expiry": {"expiryType": "END_OF_DAY"},
                    "limit": {"limit": None},
                    "quantity": order.quantity,
                    "symbol": order.symbol,
                    "transactionType": order.transaction_type
                }
            },
            "query": "mutation StockTrade($input: TradeEntityInput!) { submitStockTrade(stockTradeEntityInput: $input) { ... on TradeInvalidEntity { errorMessages __typename } ... on TradeInvalidTransaction { errorMessages __typename } __typename } }"
        }

        self.sess.post(API_URL, json=body)

    def get_holdings(self) -> List[Holding]:
        holdings = []

        for htype in ["STOCKS", "SHORTS"]:
            holdings.extend(
                self._get_holdings(htype)
            )

        return holdings

    def _get_holdings(self, holding_type: str) -> List[Holding]:
        holdings = [] 

        body = {
            "operationName": "StockHoldings",
            "variables": {
                "holdingType": holding_type,
            },
            "query": "query StockHoldings($portfolioId: String!, $holdingType: HoldingType!) { readPortfolio(portfolioId: $portfolioId) { ... on PortfolioErrorResponse { errorMessages __typename } ... on Portfolio { holdings(type: $holdingType) { ... on HoldingsErrorResponse { errorMessages __typename } ... on CategorizedHoldingsErrorResponse { errorMessages __typename } ... on CategorizedStockHoldings { holdingsSummary { marketValue dayGainDollar dayGainPercent totalGainDollar totalGainPercent __typename } executedTrades { stock { ... on Stock { symbol description technical { lastPrice __typename } __typename } __typename } symbol quantity purchasePrice marketValue dayGainDollar dayGainPercent totalGainDollar totalGainPercent __typename } __typename } __typename } __typename } __typename } }"
            }
        
        data = self.sess.post(API_URL, json=body).json()["data"]["readPortfolio"]["holdings"]["executedTrades"]

        for holding in data:
            holdings.append(
                Holding(
                    symbol=holding["symbol"],
                    quantity=holding["quantity"],
                    holding_type=holding_type
                )
            )
        
        return holdings