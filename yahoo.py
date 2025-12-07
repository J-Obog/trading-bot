from typing import List
import requests
from dataclasses import dataclass

@dataclass
class Rating:
    pass

class AnalystRatingsClient:
    def __init__(self):
        pass

    def get_ratings(self, ticker: str) -> List[Rating]:
        pass