from enum import StrEnum
from typing import Any, List, Optional
from pyairtable import Api
from dataclasses import dataclass
from datetime import datetime
from dateutil.parser import parse

class Outcome(StrEnum):
    RIGHT = "Right"
    WRONG = "Wrong"
    
@dataclass
class Prediction:
    id: str
    ticker: str
    analyst: str
    announcement_date: datetime
    price_target: float
    outcome: Outcome
    close_date: Optional[datetime]
    expiration_date: datetime


def from_dict(obj: dict[str, Any]) -> Prediction:
    return Prediction(
        id=obj["Rating ID"], 
        ticker=obj["Ticker"], 
        analyst=obj["Analyst"],    
        price_target=obj["Price Target"],
        outcome=Outcome(obj["Outcome"]) if "Outcome" in obj else None, 
        announcement_date=parse(obj["Announcement Date"], ignoretz=True), 
        close_date=parse(obj["Close Date"], ignoretz=True) if "Close Date" in obj else None,
        expiration_date=parse(obj["Expiration Date"], ignoretz=True),
    )


def to_dict(prediction: Prediction) -> dict[str, Any]:
    obj = {
    "Rating ID": prediction.id,
    "Ticker": prediction.ticker, 
    "Analyst": prediction.analyst,
    "Price Target": prediction.price_target,
    "Announcement Date": prediction.announcement_date.strftime("%m/%d/%Y"),
    "Expiration Date": prediction.expiration_date.strftime("%m/%d/%Y"),
    }

    if prediction.outcome is not None:
        obj["Outcome"] = prediction.outcome.value

    if prediction.close_date is not None:
        obj["Close Date"] = prediction.close_date.strftime("%m/%d/%Y")

    return obj

class AirtableApi:
    def __init__(self, token: str, base_id: str, tbl_id: str):
        self.api = Api(token).table(base_id, tbl_id)

    def create_predictions(self, predictions: List[Prediction]):
        self.api.batch_create([to_dict(prediction) for prediction in predictions])
        
    def get_all_predictions(self) -> List[Prediction]:
        return [from_dict(row["fields"]) for row in self.api.all()]

