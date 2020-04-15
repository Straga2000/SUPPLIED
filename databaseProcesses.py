import pymongo

class Database:
    def __init__(self, database_name= "Food Tracker", url= 'mongodb+srv://straga:zeus16hades@maincluster-aybxn.mongodb.net/test?retryWrites=true&w=majority'):

        self.client = pymongo.MongoClient(url)

        self.databaseList = None
        self.refresh_database_list()

        self.database = None
        self.create_database(database_name)

        self.collectionList = None
        self.refresh_collection_list()

    def refresh_database_list(self):
        self.databaseList = self.client.list_database_names()

    def refresh_collection_list(self):
        self.collectionList = self.database.list_collection_names()

    def create_database(self, database_name):
        self.database = self.client[database_name]
        if database_name not in self.databaseList:
            self.refresh_database_list()
            self.create_collection("dummy")

    def create_collection(self, name):
        if name not in self.collectionList:
            self.refresh_collection_list()
            self.database[name].insert_one({"type": "dummmy"})

    def insert_one_in_collection(self, name, dict):
        return self.database[name].insert_one(dict)

    def insert_multiple_in_collection(self, name, list):
        return self.database[name].insert_many(list)

    def delete_collection(self, name):
        self.database.delete_collection(name)

    def delete_insertion(self, name, dict):
        self.database[name].delete_one(dict)

    def delete_multiple_insertion(self, name, list):
        self.database[name].delete_many(list)

    def print_collection(self, name):
        for x in self.database[name].find():
            print (x)

    def query_many(self, name, query=None):
        if query is None:
            return self.database[name].find()
        else:
            return self.database[name].find({}, query)

    def query_one(self, name, query= None):
        if query is None:
            return self.database[name].find()
        else:
            return self.database[name].find({}, query)

    def count(self, name, query= None):
        if query is None:
            return self.database[name].count_documents()
        else:
            return self.database[name].count_documents(query)