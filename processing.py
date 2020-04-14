class Product:
    def __init__(self, price, quantity, time):

        self.updateCounter = 1

        self.initialPrice = price
        self.currentPrice = price
        self.currentQuantity = quantity
        self.currentTimeStamp = time

        self.totalQuantity = quantity
        self.totalPrices = price

    # def set_product(self, price, quantity, time):
    #
    #     self.currentPrice = price
    #     self.currentQuantity = quantity
    #     self.currentTimeStamp = time
    #     self.totalQuantity += quantity
    #     self.totalPrices += price

    def get_average_price(self):
        return self.totalPrices / self.updateCounter
        #Avp = average_price = sum of prices / # prices
        #se face dupa set_products

    def average_price_change(self):
        return (self.currentPrice - self.initialPrice) / self.currentTimeStamp
        #ACP = average price change = (price[i] - price[0]) / t[i]
        # se face dupa set_product

    def get_average_daily_distribution(self):
        return self.totalQuantity / self.currentTimeStamp
        #D = Average daily_Distribution = total_quantity / t[i]
        #se face dupa set_product

    def get_daily_distribution(self, quantity, time):
        return quantity / (time - self.currentTimeStamp)
        #d = Daily_distribution = quantity[i]] / (t[i] - t[i - 1])
        #se face inainte de set_product

    def get_future_price(self, time):
        return self.average_price_change() * time + self.get_average_price()
        #FP(T) = Future price = ACP * T + average_price

    def get_expense_over_a_week(self):

        avgDailyDistr = self.get_average_daily_distribution()
        return 7 * avgDailyDistr * (self.average_price_change() * (self.currentTimeStamp + 4) + self.get_average_price())
        # e(x) = Expense of product x over a week = FP(T+1) * D + FP(T + 2) * D +... + FP(T+7) * D
        # e(x) = D * (SUM(FP(T + i), 1, 7))
        # e(x) = D * (SUM(ACP * (T + i) + average_price), 1, 7)
        # e(x) = D * (ACP * (SUM(T + i, 1, 7)) + 7 * average_price)
        # e(x) = D * (ACP * (7 * T + 28) + 7 * average_price)
        # e(x) = D * (ACP * 7 * (T + 4) + 7 * average_price)
        # e(x) = 7 * D * (ACP * (T + 4) + average_price)

    def update_product(self, price = None, quantity = None, time = None):

        if price is None:
            price = self.currentPrice
        if quantity is None:
            quantity = self.currentQuantity
        if time is None:
            time = self.currentTimeStamp

        timeDiff = self.currentTimeStamp - time

        dailyDistribution = quantity / timeDiff

        newPriceDerivateValue = (self.currentPrice - price) / timeDiff

        self.set_product(price, quantity, time)

    def get_average_quantity(self):
        calc = 0

        for elem in self.quantityList:
            calc += elem[0] * elem[1]

        return  calc / self.totalQuantitySum

class ProductList:
    def __init__(self):
        self.productList = {}

    def add_product(self, name, price, quantity, time):

        if self.productList.get(name) is None:
            self.productList[name] = Product(price, quantity, time)
        else:
            self.productList[name].update_product(price, quantity, time)

    def get_product(self, name):
        if self.productList.get(name) is not None:
            return self.productList[name]
        else:
            return None

    def