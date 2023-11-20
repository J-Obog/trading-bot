from dataclasses import dataclass
from enum import StrEnum

class OrderType(StrEnum):
    BUY = "buy"
    SELL = "sell" 
    SHORT = "short"
    BUY_TO_COVER = "buy_to_cover" 

class Order:
    quantity: int
    symbol: str
    order_type: OrderType

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
class HoldingType(StrEnum):
    LONG = "long"
    SHORT = "short" 


class Holding:
    symbol: str
    quantity: int
    holding_type: HoldingType


class StockRatingType(StrEnum):
    STRONG_BUY = "strong_buy"
    BUY = "buy"
    HOLD = "hold"
    SELL = "sell" 
    STRONG_SELL = "strong_sell"


class StockRating:
    rating: StockRatingType
    rating_entities: set[str]