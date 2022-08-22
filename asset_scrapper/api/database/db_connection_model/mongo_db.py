#Ghetto way to get higher level parent directories imported
import json
import os, sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
for i in range(2):
    parentdir = os.path.dirname(parentdir)
sys.path.append(parentdir)
from utils.errors import DatabaseError
from utils.util import parse_json
from .no_sql_database import Database
from pymongo import MongoClient
class Mongo(Database):

    def __init__(self):
        self.__client = None
        self.__db = None
        self.test = "hey"


    def connect(self, config: dict): #CHANGE THIS TO ACCEPT CONFIG 
        """
        Allows for explicit connection mapping

        Args:
            username (str): _description_
            password (str): _description_
            server (str): _description_
            db_name (str): _description_

        Raises:
            DatabaseError: _description_
        """
        CONNECTION_STR = f"mongodb+srv://{config['username']}:{config['password']}@{config['server']}.mongodb.net/?retryWrites=true&w=majority"
        self.__client = MongoClient(CONNECTION_STR)
        if self.__client.list_database_names().count(config['db_name']) == 0:
            raise DatabaseError("Database does not exist")
        
        self.__db = self.__client[config['db_name']]
        # return self.__db
    

    def push_data(self, collection: str, data):
        """_summary_

        Args:
            collection (str): The collection name to save the data to
            data (_type_): an object that will be pushed to mongodb
        """

        return parse_json(self.__get_db()[collection].insert_one(data).inserted_id)



    def get_data(self, collection: str, filter: str):
        if(self.check_collection_exist(collection_name=collection)):
            return self.__db[collection].find_one(filter=filter)
        else:
            raise DatabaseError("collection does not exist")
    
    def __get_db(self):
        if not self.__db is not None:
            raise DatabaseError("DB not initialized")
        return self.__db

    def check_collection_exist(self,collection_name: str):
        if(self.__get_db().list_collection_names().count(collection_name) == 0):
            return False
        return True
    
    def close_db(self):
        if self.__get_db() is not None:
            self.__get_db().__client.close()


   
# a = Mongo( )
# a.connect("Mike", "Summer2022.","stocktrack.7e2q0by", "firstDB3")
# a.push_data("collect",{'test': {"hey":1}})


