from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

class DBService:
    db_service = MongoClient(os.getenv("MONGODB_URI"))
    db = db_service["FastAPI"]
    auth = db["auth"]
