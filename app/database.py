from pymongo import MongoClient
from fastapi import Depends
from decouple import config

# Replace these with your actual MongoDB server URL and database name
DB_URL = config("APP_DB_URL")
DB_NAME = "YOUR_DB_NAME"

client = MongoClient(DB_URL)
db = client[DB_NAME]

# Dependency to provide the MongoDB database connection
def get_db():
    try:
        yield db
    finally:
        client.close()
