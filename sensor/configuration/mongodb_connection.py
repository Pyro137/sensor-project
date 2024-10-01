import pymongo
from sensor.constant.database import DATABASE_NAME
from sensor.logger import logging
import certifi
import os
from dotenv import load_dotenv




ca = certifi.where()

class MongoDBClient:
    client = None
    def __init__(self, database_name=DATABASE_NAME) -> None:
        try:

            if MongoDBClient.client is None:
                if "localhost" in "mongodb+srv://Metin:kyLD2YoeVZTJZB5c@cluster0.fllviyo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0":
                    MongoDBClient.client = pymongo.MongoClient("mongodb+srv://Metin:kyLD2YoeVZTJZB5c@cluster0.fllviyo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0") 
                else:
                    MongoDBClient.client = pymongo.MongoClient("mongodb+srv://Metin:kyLD2YoeVZTJZB5c@cluster0.fllviyo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0", tlsCAFile=ca)
            self.client = MongoDBClient.client
            self.database = self.client[database_name]
            self.database_name = database_name
            logging.info(f"Connection to MongoDB is successful")
        except Exception as e:
            raise e
