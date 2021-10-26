#!Python 3
import os
import traceback
from pathlib import Path
from typing import List, Union
import pyinputplus as pyip

from bson.objectid import ObjectId
from pymongo.results import InsertOneResult, UpdateResult
from pymongo.collection import Collection
from pymongo import MongoClient
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

MONGO_URI = f"mongodb://vashlt:{os.getenv('DB_PASSWORD')}@cluster0-shard-00-00.0co7e.mongodb.net:27017,cluster0-shard-00-01.0co7e.mongodb.net:27017,cluster0-shard-00-02.0co7e.mongodb.net:27017/{os.getenv('DB_NAME')}?replicaSet=atlas-dwxv6c-shard-0&ssl=true&authSource=admin"

COLLECTION_NAME = "users"


class Database:
    def __init__(self):
        self._client = MongoClient(MONGO_URI)
        self._db = self._client.get_database()

    def get_user(self, cc: int) -> Union[dict, bool]:
        collection: Collection = self._db[COLLECTION_NAME]
        try:
            return collection.find_one({"cc": cc})
        except:
            print(f"[db.get_user] failed!\n {traceback.print_exc()}")
            return False

    def exists(self, cc: int) -> bool:
        """check existence of an user by their cc"""
        collection = self._db[COLLECTION_NAME]
        try:
            return collection.count_documents({"cc": int(cc)}, limit=1) > 0

        except:
            print(f"[db.exists] failed!\n {traceback.print_exc()}")
            return False

    def register(
        self, cc: int, name: str, money: float = 0
    ) -> Union[InsertOneResult, bool]:
        collection: Collection = self._db[COLLECTION_NAME]

        try:
            insert_dict = {
                "cc": cc,
                "name": name,
                "money": money,
                "joined_date": datetime.now(),
                "transactions": [],
            }
            result = collection.insert_one(insert_dict)

        except:
            print(f"[db.register] failed!\n {traceback.print_exc()}")
            return False

        return result

    def add_money(self, cc: int, money: float) -> Union[UpdateResult, bool]:
        """add money and message"""
        collection: Collection = self._db[COLLECTION_NAME]
        try:
            message = pyip.inputStr(prompt="Message (Mandatory): ", limit=3)
        except pyip.RetryLimitException:
            print("[INFO] Limit of attempts exceeded.")

        print(
            f"""[IN PROGRESS] {"Adding" if money >= 0 else "Substracting"} money ..."""
        )

        update_dict = {
            "$inc": {"money": money},
        }

        try:
            result = collection.update_one({"cc": cc}, update_dict)
            self.update_history(cc, message, money)

        except:
            print(f"[db.add_money] failed!\n {traceback.print_exc()}")
            return False

        return result

    def update_history(
        self, cc: int, reason: str, money: float
    ) -> Union[UpdateResult, bool]:
        collection: Collection = self._db[COLLECTION_NAME]
        if not (user := collection.find_one({"cc": cc})):
            print(f"[db.update_history] failed!\n {traceback.print_exc()}")
            return False

        update_dict = {
            "$push": {
                "transactions": {
                    "_id": ObjectId(),
                    "date": datetime.now(),
                    "amount": money,
                    "message": reason,
                    "total": user["money"],
                }
            }
        }

        try:
            result = collection.update_one({"cc": cc}, update_dict)
        except:
            print(f"[db.update_history] failed!\n {traceback.print_exc()}")
            return False

        return result

    def get_history(self, cc: int) -> Union[List[dict], bool]:
        collection: Collection = self._db[COLLECTION_NAME]
        try:
            user = collection.find_one({"cc": cc})
        except:
            print(f"[db.get_history] failed!\n {traceback.print_exc()}")
            return False

        return user["transactions"]


if __name__ == "__main__":
    print(Database().add_money(1000233215, 100.5))
