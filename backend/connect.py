from flask_pymongo import pymongo
from pymongo.mongo_client import MongoClient
from config import config

# Use configuration from config.py
MONGO_URI = config.get_mongo_uri()
DATABASE_NAME = config.get_database_name()

# Create MongoDB connection
client = MongoClient(MONGO_URI)
db = client.get_database(DATABASE_NAME)
users = pymongo.collection.Collection(db, 'users')