from dataclasses import dataclass

@dataclass
class Order:
    quantity: int
    symbol: str
    transaction_type: str