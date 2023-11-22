from __future__ import annotations
from enum import StrEnum
from dataclasses import dataclass

@dataclass
class TopCompany:
    symbol: str

class OrderType(StrEnum):
    BUY = "buy"
    SELL = "sell" 
    SHORT = "short"
    BUY_TO_COVER = "cover"
     
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
    cost_basis: float
    market_value: float


class StockRatingType(StrEnum):
    BUY = "buy"
    HOLD = "hold"
    SELL = "sell" 


@dataclass
class StockRating:
    rating: StockRatingType
    rating_entities: set[str]