import requests

from trading.data import Order

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