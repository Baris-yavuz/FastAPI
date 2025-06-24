from pymongo import MongoClient, ReturnDocument
import os
from dotenv import load_dotenv

load_dotenv()


class DBService:
    db_service = MongoClient(os.getenv("MONGODB_URI"))
    db = db_service["FastAPI"]
    auth = db["auth"]
    admin = db["admin"]
    counters = db["counters"]


    @staticmethod
    def get_next_admin_id():
        result = DBService.counters.find_one_and_update(
            {"_id": "admin_id"},
            {"$inc": {"sequence_value": 1}},
            return_document=ReturnDocument.AFTER,
            upsert=True
        )
        return result["sequence_value"]


    @staticmethod
    def get_next_user_id():
        result = DBService.counters.find_one_and_update(
            {"_id": "user_id"},
            {"$inc": {"sequence_value": 1}},
            return_document=ReturnDocument.AFTER,
            upsert=True
        )
        return result["sequence_value"]


class Settings:
    SECRET_KEY: str = os.getenv("SECRET_KEY", "default_key") 

settings = Settings()


