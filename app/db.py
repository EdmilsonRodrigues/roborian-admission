import motor.motor_asyncio as motor_asyncio
from pymongo import MongoClient
from load_dotenv import load_dotenv
from os import getenv

load_dotenv()

MONGO_URI = getenv("MONGO_URI")


# Function to get MongoDB client
def get_mongo_client():
    client = motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    return client


# Function to get MongoDB database
def get_db():
    client = get_mongo_client()
    return client

