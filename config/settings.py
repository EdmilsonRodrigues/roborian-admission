import os

class Config:
    # Mongo configuration
    MONGODB_SETTINGS = {
        "db":"your_database_name",
        "host":"localhost",
        "port":27017
    }
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key"
