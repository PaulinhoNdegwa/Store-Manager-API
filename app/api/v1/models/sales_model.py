products = []
sales = []
users = []

class Sale():
    """This class initialized a sales object. 
    Also it has a save method that saves the sale in a list"""

    def __init__(self, product_name, product_price, quantity, total_price, attendant):
        """Method to initialize sales"""
        self.product_name = product_name
        self.product_price = product_price
        self.quantity = quantity
        self.total_price = total_price
        self.attendant =  attendant

    def save_sale(self):
        
        sale_id = len(sales) + 1
        sale = {
            "sale_id": sale_id,
            "product_name": self.product_name,
            "product_price": self.product_price,
            "quantity": self.quantity,
            "total_price": self.total_price,
            "attendant": self.attendant
        }
        sales.append(sale)
        return sale
