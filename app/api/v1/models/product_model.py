products = []
sales = []
users = []

class Product():
    """This class initialized a sales object. 
    Also it has a save method that saves the sale in a list"""

    def __init__(self, product_name, product_price, quantity, min_quantity):
        """Method to initialize Product objects"""
        self.quantity = quantity
        self.min_quantity = min_quantity
        self.product_name = product_name
        self.product_price = product_price

    def save_product(self):
        """Method to create and save a product dict object"""
        if len(products) == 0:
            product_id= 1
        else:
            product_id = products[-1]["product_id"] + 1
        product = {
            "product_id": product_id,
            "product_name": self.product_name,
            "product_price": self.product_price,
            "quantity": self.quantity,
            "min_quantity": self.min_quantity
        }
        products.append(product)
        return product

