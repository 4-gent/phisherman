from flask_pymongo import pymongo
from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.environ['MONGO_URI']

client = MongoClient(MONGO_URI)
db = client.get_database('phish')
users = pymongo.collection.Collection(db, 'users')