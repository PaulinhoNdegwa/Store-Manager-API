products = []


class Product():
    """This class initialized a product object.
    Also it has a save method that saves the sale in a list"""

    def __init__(self):
        """Method to initialize Product list"""
        # self.products = products
        pass

    def save_product(self, product_name, product_price, quantity,
                     min_quantity):
        """Method to create and save a product dict object"""

        product_id = len(products) + 1
        product = {
            "product_id": product_id,
            "product_name": product_name,
            "product_price": product_price,
            "quantity": quantity,
            "min_quantity": min_quantity
        }
        products.append(product)
        return product

    def get_all_products(self):
        return products

    def get_single_product(self, product_id):
        product = [product for product in products
                   if product["product_id"] == product_id]
        return product
