sales = []


class Sale():
    """This class initialized a sales object.
    Also it has a save method that saves the sale in a list"""

    def __init__(self):
        """Method to initialize sales"""
        pass

    def save_sale(self, product_name, product_price, quantity, total_price,
                  attendant):

        sale_id = len(sales) + 1
        sale = {
            "sale_id": sale_id,
            "product_name": product_name,
            "product_price": product_price,
            "quantity": quantity,
            "total_price": total_price,
            "attendant": attendant
        }
        sales.append(sale)
        return sale

    def get_single_sale(self, sale_id):
        """Method to get single sale"""
        single_sale = [sale for sale in sales if sale["sale_id"] == sale_id]
        return single_sale

    def get_all_sales(self):
        """Method to return all products"""
        return sales
