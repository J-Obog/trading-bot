from abc import ABC
from typing import List

from trading.data import Holding

class SpreadsheetClient(ABC):
    def build_holdings_sheet(self, holdings: List[Holding]):
        ...