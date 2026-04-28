from dataclasses import dataclass
from pymongo import MongoClient
from pymongo.collection import Collection

from src.db.models import Analyst, Prediction

class Db:
    def __init__(self, conn: MongoClient):
        self._conn = conn
        database = conn["analysis"]
        self.analysts: Collection[Analyst] = database["analysts"]
        self.predictions: Collection[Prediction] = database["predictions"]

    def close(self):
        self._conn.close()

def get_db(connection_str: str) -> Db:
    client = MongoClient(connection_str)
    return Db(client)
