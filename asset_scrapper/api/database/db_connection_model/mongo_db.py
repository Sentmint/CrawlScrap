from database import Database
from pymongo import MongoClient

class Mongo(Database):

    def __init__(self):
        self.client = None
        self.db = None


    def connect(self, username: str, password: str, server: str, db_name: str):
        CONNECTION_STR = f"mongodb+srv://{username}:{password}@{server}.mongodb.net/{db_name}"
        self.client = MongoClient(CONNECTION_STR)
        self.db = self.client[db_name]
        return self.db
    
    def push(self, location: str, data):
        """_summary_

        Args:
            location (str): The collection name to save the data to
            data (_type_): an object that will be pushed to mongodb
        """
        self.db[location].insert_one(data)