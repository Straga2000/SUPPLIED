# de la product la dict
import numpy as np
from databaseProcesses import *

timeLengths = {"DAY": 1, "WEEK": 7, "MONTH": 28}
absoluteTime = 1
important_category = ("apa", "medicamente")


def updateTime(type=timeLengths["DAY"]):
    global absoluteTime
    value = 0

    for key in timeLengths:
        if type == key:
            value = timeLengths[key]

    absoluteTime += value

    return absoluteTime


'''  ----------------------------------------- PRODUCT --------------------------------------- '''


class Product:
    def __init__(self, category='', name='', price=0.0, quantity=0, time=0):
        self.updateCounter = 1
        self.category = category
        self.priority = 5
        # on a scale from 1 to 10

        self.name = name

        self.totalQuantity = quantity
        self.totalPrices = price

        self.quantity = [quantity]
        self.timeStamp = [time]
        self.prices = [price]

    def set_product(self, price, quantity, time):

        self.quantity += [quantity]

        self.totalQuantity += quantity
        self.totalPrices += price

        self.prices += [price]
        self.timeStamp += [time]

    def update_product(self, price=None, quantity=None, time=None):

        if price is None:
            price = self.prices[self.updateCounter - 1]
        if quantity is None:
            quantity = self.quantity[self.updateCounter - 1]
        if time is None:
            time = self.timeStamp[self.updateCounter - 1]
        self.updateCounter += 1
        self.set_product(price, quantity, time)

    def get_average_price(self):

        return self.totalPrices / self.updateCounter
        # Avp = average_price = sum of prices / # prices
        # se face dupa set_products

    def average_price_change(self):
        if self.timeStamp[self.updateCounter - 1] == self.timeStamp[0]:
            return 0
        return (self.prices[self.updateCounter - 1] - self.prices[0]) / \
               (self.timeStamp[self.updateCounter - 1] - self.timeStamp[0])
        # ACP = average price change = (price[i] - price[0]) / (t[i] - t[0])
        # se face dupa set_product

    def get_average_daily_distribution(self):
        if absoluteTime == self.timeStamp[0]:
            return 0
        
        return (self.totalQuantity - self.quantity[self.updateCounter - 1]) / \
               (absoluteTime - self.timeStamp[0])
        # D = Average daily_Distribution = total_quantity without the last buy / (time passed from the first buy)
        # se face dupa set_product

    def get_days_until_empty(self):
        avg = self.get_average_daily_distribution()
        if avg != 0:
            if (round(self.quantity[len(self.quantity) - 1] // avg)  - (absoluteTime - self.timeStamp[len(self.timeStamp) - 1])) < 0:
                return 0
            else:
                return (round(self.quantity[len(self.quantity) - 1] // avg)  - (absoluteTime - self.timeStamp[len(self.timeStamp) - 1]))

    def get_future_price(self, time):

        # returneaza coeficientii polinomului de interpolare
        def coeficiente(x, y):

            x = np.array(x, dtype=np.float32)
            y = np.array(y, dtype=np.float32)
            n = len(x)
            F = np.zeros((n, n), dtype=float)
            b = np.zeros(n)
            for i in range(0, n):
                F[i, 0] = y[i]
            for j in range(1, n):
                for i in range(j, n):
                    F[i, j] = float(F[i, j - 1] - F[i - 1, j - 1]) / float(x[i] - x[i - j])
            for i in range(0, n):
                b[i] = F[i, i]
            return np.array(b)  # return an array of coefficient

        # returneaza valoarea polinomului de interpolare in punctul r
        def eval(x, y, r):
            a = coeficiente(x, y)
            a.astype(float)
            n = len(a) - 1
            temp = a[n]
            for i in range(n - 1, -1, -1):
                temp = temp * (r - x[i]) + a[i]
            return abs(temp)  # return the y_value interpolation

        return eval(self.timeStamp, self.prices, time)
        # returneaza pretul unui obiect la momentul de timp time

    def get_expense_over_a_week(self):

        avgDailyDistr = self.get_average_daily_distribution()
        ans = 0.0


        for index in range(1, 8):
            ans += avgDailyDistr * self.get_future_price(absoluteTime + index)
        return abs(ans)
        # e(x) = Expense of product x over a week = FP(T+1) * D + FP(T + 2) * D +... + FP(T+7) * D

    def update_priority(self, value):
        self.priority += value
        if self.priority > 10 :
            self.priority = 10
        if self.priority < 0:
            self.priority = 0

    def set_priority(self, value):
        self.priority = value

    def to_dict(self):
        ans = dict()
        ans['updateCounter'] = self.updateCounter
        ans['totalQuantity'] = self.totalQuantity
        ans['totalPrices'] = self.totalPrices
        ans['quantity'] = self.quantity
        ans['timeStamp'] = self.timeStamp
        ans['prices'] = self.prices
        ans['name'] = self.name
        return ans

    def set_from_dict(self, obj):
        self.updateCounter = obj['updateCounter']
        self.totalQuantity = obj['totalQuanitity']
        self.totalPrices = obj['totalPrices']
        self.quantity = obj['quantity']
        self.timeStamp = obj['timeStamp']
        self.prices = obj['prices']
        self.name = obj['name']


'''  ----------------------------------------- PRODUCTLIST ---------------------------------------  '''


class ProductList:
    def __init__(self):
        self.productList = {}

    def add_product(self, category, name, price, quantity, time):
        global absoluteTime

        absoluteTime = time

        if self.productList.get(name) is None:
            self.productList[name] = Product(category, name, price, quantity, time)  
            # if the product is water or meds, set the priority to max
            if category in important_category[0] or category in important_category[0]:
                self.productList[name].set_priority(10)
        else:
            self.productList[name].update_product(price, quantity, time)

    def get_days_until_empty(self):
        ans = dict()
        for key in self.productList.keys():
            ans[key] = self.productList[key].get_days_until_empty()
        return ans

    def get_product(self, name):
        if self.productList.get(name) is not None:
            return self.productList[name]
        else:
            return None

    def delete_product(self, name):
        self.productList[name] = None

    def filter(self, type="None"):
        value = 0
        for key in timeLengths:
            if type == key:
                value = timeLengths[key]

        if value == 0:
            return self.productList
        else:
            newList = {}

            for key in self.productList:
                if self.productList[key].get_average_daily_distribution() >= value:
                    newList[key] = self.productList[key]
            return newList

    def to_dict(self):
        ans = dict()
        for key in self.productList.keys():
            ans[key] = self.productList[key].to_dict()
        return ans

    def set_from_dict(self, obj):
        for key in obj:
            self.productList[key] = Product()
            self.productList[key].set_from_dict(obj[key])

    # -------------------------------- expense methods ---------------------------
    def get_expense_over_a_week(self):
        ans = 0.0
        for item in self.productList.keys():

            ans += self.productList[item].get_expense_over_a_week()

        return ans

    def get_expense_over_a_month(self):
        return 4 * self.get_expense_over_a_week()


''' ---------------------------------------- USER -------------------------------------------- '''


class User:
    def __init__(self, first_name='', last_name='', email='', id='', password_hash='', budget=0.0, product_list = None):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.id = id
        self.password_hash = password_hash
        self.budget = budget

        if product_list is None:
            self.product_list = ProductList()
        else:
            self.product_list = product_list

    def to_dict(self):
        return {"first_name": self.first_name, "last_name": self.last_name, "email": self.email, "id": self.id,
                "pass": self.password_hash, "budget": self.budget, "product_list": self.product_list.to_dict()}

    def set_from_dict(self, obj):
        self.first_name = obj["first_name"]
        self.last_name = obj["last_name"]
        self.email = obj["email"]
        self.id = obj["id"]
        self.password_hash = obj["pass"]
        self.budget = obj["budget"]
        self.product_list.set_from_dict(obj["product_list"].set_from_dict())

    def update_budget(self, val):
        self.budget = val

    def add_item(self, category, name, price, quantity, time):

        self.product_list.add_product(category, name, price, quantity, time)

    def get_days_until_empty(self):
        return self.product_list.get_days_until_empty()

    def get_remove_suggestion(self):
        expense = self.product_list.get_expense_over_a_month()

        if self.budget >= self.product_list.get_expense_over_a_month():
            return "Well done!!!"
        else:
            vec = []
            for it in self.product_list.productList.keys():
                vec += [(self.product_list.productList[it].name, self.product_list.productList[it].priority,
                         self.product_list.productList[it].get_average_daily_distribution(),
                         self.product_list.productList[it].get_average_price())]
            vec.sort(key=lambda x: (x[1], x[2], x[3]))

            ans = []
            sum = 0.0

            for item in vec:
                if sum + self.budget > expense:
                    return ans
                response = 0
                if (self.product_list.get_product(item[0]).priority < 0):
                    #auto delete the item
                    response = 1
                else:
                    pass
                    # o sa intrebam userul daca e de acord cu stergerea produsului
                    # response = get_swipe(self.product_list.get_product(item[0]))
                if response == 1:
                    self.product_list.get_product(item[0]).update_priority(-1)
                    sum += self.product_list.get_product(item[0]).get_expense_over_a_week() * 4
                    ans += [item]
                else:
                    self.product_list.get_product(item[0]).update_priority(1)
            return ans

    def print_removed_items(self):
        response = self.get_remove_suggestion()

        if response == 'Well done!!!':
            print("No need to remove items")
        else:
            print("Items to be removed from your shopping list")
            for it in response:
                print(it[0])


# user = User("Bob", "bob", "Bob", "Bob", "Bob", 14444.0)
# user.add_item("apa", "borsec", 1.0, 5, absoluteTime)
# updateTime("DAY")
# user.add_item("apa", "borsec", 1.0, 5, absoluteTime)
# updateTime("DAY")
# user.add_item("apa", "borsec", 1.0, 5, absoluteTime)
# updateTime("DAY")
# user.add_item("apa", "borsec", 1.0, 5, absoluteTime)
# updateTime("DAY")
# user.add_item("mancare", "pui", 50.0, 1, absoluteTime)
# updateTime("DAY")
# user.add_item("mancare", "pui", 50.0, 5, absoluteTime)
# user.print_removed_items()