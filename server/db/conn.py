from dataclasses import dataclass
from pymongo import MongoClient
from pymongo.collection import Collection

from server.db.models import Analyst, Prediction

@dataclass
class Db:
    analysts: Collection[Analyst]
    predictions: Collection[Prediction]


def get_db(connection_str: str) -> Db:
    client = MongoClient(connection_str)
    database = client["analysis"]
    return Db(
        analysts=database["analysts"],
        predictions=database["predictions"]
    )