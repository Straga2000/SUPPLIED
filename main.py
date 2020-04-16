from processing import *
from WebScraper import *
from databaseProcesses import *
from hashlib import *

class siteFunctions:
    def __init__(self):

        self.siteEmail = 'food.tracker.prices@gmail.com'
        self.sitePassword = 'mqgjzndoxjhmlzbk'

        #self.database = Database()
        #self.database.create_collection("users")
        self.userList = {}

    def security(self, name):
        return name
        #return sha256(name.encode()).hexdigest()

    def login_user(self, email='', password_hash=''):
        id = self.security(password_hash)
        '''
        obj = self.database.query_one("users", {"id": id})
        if obj is not None:
            self.userList[id] = User()
            self.userList[id].set_from_dict(obj)
            return id
        else:
            return None
        '''
    def logout_user(self, id=''):
        self.userList[id] = None

    def add_user(self, first_name='', last_name='', email='', password_hash=''):
        id = self.security(password_hash)
        user = User(first_name, last_name, email, id, password_hash)
        self.userList[id] = user
        #self.database.insert_one_in_collection("users", user.to_dict())

    def add_product(self, id, category, name, price, quantity, time):
        self.userList[id].add_item(category, name, price, quantity, time)

    def delete_product(self, id, name):
        return self.userList[id].product_list.delete_product(name)

    def get_week_forecast(self, id):
        return self.userList[id].product_list.get_expense_over_a_week()

    def get_month_forecast(self, id):
        return self.userList[id].product_list.get_expense_over_a_month()

    def get_email_by_search(self, id, objList):
        userEmail = self.userList[id].email
        send_mail(objList, self.siteEmail, self.sitePassword, userEmail)


Site = siteFunctions()

Site.add_user("Bob","Bob","Bob@gmail.com","Bob")
Site.add_product(Site.security("Bob"), "apa", "Borsec", 1.0, 2, 2)
Site.add_product(Site.security("Bob"), "apa", "Borsec", 1.0, 2, 3)
Site.add_product(Site.security("Bob"), "apa", "Borsec", 1.0, 2, 4)
print(Site.get_week_forecast(Site.security("Bob")))
