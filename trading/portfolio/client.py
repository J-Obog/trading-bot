from abc import ABC
from typing import List

from trading.data import Holding, Order

class PortfolioClient(ABC):
    def place_order(self, order: Order):
        ...
        
    def get_pending_orders(self) -> List[Order]:
        ...

    def get_holdings(self) -> List[Holding]:
        ...