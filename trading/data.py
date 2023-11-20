from dataclasses import dataclass

@dataclass
class Order:
    quantity: int
    symbol: str
    transaction_type: str # should be an enum

"""
{
    "stock": {
        "symbol": "BRK.A",
        "description": "Berkshire Hathaway Inc. - Ordinary Shares - Class A",
        "technical": {
            "lastPrice": 544190,
            "__typename": "Technical"
        },
        "__typename": "Stock"
    },
    "symbol": "BRK.A",
    "quantity": 199304286,
    "purchasePrice": 522669.58,
    "marketValue": 108459399398340,
    "dayGainDollar": 0,
    "dayGainPercent": 0,
    "totalGainDollar": 4289112402833.55,
    "totalGainPercent": 4.12,
    "__typename": "ExecutedStockHolding"
}
"""

@dataclass
class Holding:
    symbol: str
    quantity: int
    holding_type: str # should be enum


@dataclass
class StockRating:
    rating: str
    rating_entities: set[str]