class Product:
    def __init__(self, price, quantity, time):

        self.priceList = []
        self.quantityList = []

        self.currentPrice = price
        self.currentQuantity = quantity
        self.currentTimeStamp = time

        self.totalQuantitySum = quantity

    def set_product(self, price, quantity, time):

        self.currentPrice = price
        self.currentQuantity = quantity
        self.currentTimeStamp = time
        self.totalQuantitySum += quantity

    def update_product(self, price, quantity, time):

        timeDiff = self.currentTimeStamp - time

        newQuantityValue = quantity / timeDiff
        newPriceDerivateValue = (self.currentPrice - price) / timeDiff

        self.quantityList.append((newQuantityValue, quantity))
        self.priceList.append(newPriceDerivateValue)

        self.set_product(price, quantity, time)

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
        else return None

