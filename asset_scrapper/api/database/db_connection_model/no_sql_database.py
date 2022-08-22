import json


class Database:

    def __init__(self):
        pass
    
    def push_data(self, location: str, data: dict) -> bool: #For relational DBs, location would be schema. for noSQL, it is document path
        pass

    def get_data(self, location: str, filter: dict) -> dict:
        pass
    
    def connect(self, username: str, password: str, server: str, db_name: str):
        pass

    def get_db(self):
        pass

    def create_collection(self, collection_name: str):
        pass