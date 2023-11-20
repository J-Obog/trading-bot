from enum import StrEnum
from dataclasses import dataclass

@dataclass
class TopCompany:
    symbol: str

class OrderType(StrEnum):
    BUY = "buy"
    SELL = "sell" 
    SHORT = "short"
    BUY_TO_COVER = "buy_to_cover" 

@dataclass
class Order:
    quantity: int
    symbol: str
    order_type: OrderType

class HoldingType(StrEnum):
    LONG = "long"
    SHORT = "short" 

@dataclass
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

@dataclass
class StockRating:
    rating: StockRatingType
    rating_entities: set[str]