from sensor.configuration.mongodb_connection import MongoDBClient

if __name__ == "__main__":
    mongodb_client = MongoDBClient()
    print("MongoDB Client is created")
    print(mongodb_client.database.list_collection_names())
