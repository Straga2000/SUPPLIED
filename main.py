from processing import *
from WebScraper import *
from databaseProcesses import *
from hashlib import *

class siteFunctions:
    def __init__(self):
        self.database = Database()
        self.database.create_collection("users")
        self.userList = {}

    def security(self, name):
        return sha256(name.encode()).hexdigest()

    def login_user(self, email='', password_hash=''):
        id = self.security(password_hash)
        self.userList[id] = self.get_user_data(id)

    def add_user(self, first_name='', last_name='', email='', password_hash=''):
        id = self.security(password_hash)
        user = User(first_name, last_name, email, id, password_hash)
        self.database.insert_one_in_collection("users", user.to_dict())

    def get_user_data(self, id = ''):
        obj =  self.database.query_one("users", {"id": id})
        if obj is not None:
            user = User()
            user.set_from_dict(obj)
            return user
        else:
            return None

    def add_product(self, id, category, name, price, quantity, time):
        user = self.get_user_data(id)
        user.product_list.add_product(category, name, price, quantity, time)

    def delete_product(self, id, name):
        user = self.get_user_data(id)
        user.product_list.delete_product(name)