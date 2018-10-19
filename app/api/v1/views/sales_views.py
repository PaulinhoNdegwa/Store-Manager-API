from flask import abort, jsonify, request
from flask_restful import  Resource
from ..models.sales_model import Sale, sales
from ..models.product_model import products
from flask_jwt_extended import jwt_required
    
class Sales(Resource):
    """This class provides access to operations to GET and POST on sales"""
    @jwt_required
    def get(self):
        """Gets all sales orders"""
        return jsonify({"Sales": sales,
                        "status":200})
    @jwt_required
    def post(self):
        """Saves a new sales order"""
        # sale_id = uuid.uuid1()
        product_name = request.get_json("product_name")["product_name"].strip(" ")
        product_price = int(request.get_json("product_price")["product_price"])
        quantity = int(request.get_json("quantity")["quantity"])
        attendant = request.get_json("attendant")["attendant"].strip(" ")
        total_price = product_price * quantity
       
        if product_name=="" or not product_name:
            abort(400)
        
        if not request.json:
            abort(400)

        product_available = [product for product in products if product_name == product["product_name"]]

        excess_order = [product for product in product_available if quantity > (product["quantity"] - product["min_quantity"])]

        if len(product_available) == 0:
            # abort(400)
            return jsonify({"message":"Product not available",
                            "status":404})
        elif len(excess_order) > 0:
            return jsonify({"message":"Forbidden: There are fewer products than requested",
                            "status":403})
        else:
            sale = Sale(product_name, product_price, quantity, total_price, attendant)
            newsale = sale.save_sale()
            return jsonify({"Message":"Successfully saved",
                            "Sale recorded": newsale,
                            "status": 201})

class SingleSale(Resource):
    """This resource will be used by the api to fetch specific sale"""
    @jwt_required
    def get(self, sale_id):
        """Gets a single sale order"""
        if not isinstance(sale_id, int) or not sale_id:
            abort(404)
        sale  = [sale for sale in sales if sale_id == sale["sale_id"]]
        if len(sale) == 0:
            return jsonify({"message":"Sale not found",
                            "status": 404})
        else:
            return jsonify({"Sale" : sale,
                            "status" : 200})
                            