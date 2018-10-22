from flask import abort, jsonify, request
from flask_restful import  Resource
from ..models.sales_model import Sale
from ..models.product_model import products
from flask_jwt_extended import jwt_required
    
class Sales(Resource, Sale):
    """This class provides access to operations to GET and POST on sales"""

    def __init__(self):
        # self.sale = Sale()
        pass

    @jwt_required
    def get(self):
        """Gets all sales orders"""
        return jsonify({"Sales": self.get_all_sales(),
                        "status":200})
    @jwt_required
    def post(self):
        """Saves a new sales order"""
        
        product_name = request.get_json("product_name")["product_name"].strip(" ")
        product_price = int(request.get_json("product_price")["product_price"])
        quantity = int(request.get_json("quantity")["quantity"])
        attendant = request.get_json("attendant")["attendant"].strip(" ")
        total_price = product_price * quantity
       
        if product_name=="" or not product_name:
            return jsonify({"message":"You must provide product details",
                            "status":400})
        
        if not request.json:
            return jsonify({"message":"Input should be in json format",
                            "status":400})

        product_available = [product for product in products if product_name == product["product_name"]]

        excess_order = [product for product in product_available if quantity > (product["quantity"] - product["min_quantity"])]

        if len(product_available) == 0:
            return jsonify({"message":"Product not available",
                            "status":404})
        elif len(excess_order) > 0:
            return jsonify({"message":"Forbidden: There are fewer products than requested",
                            "status":403})
        else:
            newsale = self.save_sale(product_name, product_price, quantity, total_price, attendant)
            return jsonify({"Message":"Successfully saved",
                            "Sale recorded": newsale,
                            "status": 201})

class SingleSale(Resource, Sale):
    """This resource will be used by the api to fetch specific sale"""

    def __init__(self):
        pass


    @jwt_required
    def get(self, sale_id):
        """Gets a single sale order"""
        if not isinstance(sale_id, int) or not sale_id:
            return jsonify({"message":"Please provide a valid sale id(int)",
                            "status":404})
        sale  = self.get_single_sale(sale_id)
        if len(sale) == 0:
            return jsonify({"message":"Sale not found",
                            "status": 404})
        else:
            return jsonify({"Sale" : sale,
                            "status" : 200})
                            