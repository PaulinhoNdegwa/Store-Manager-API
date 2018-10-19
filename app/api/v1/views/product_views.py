from flask import abort, jsonify, request
from flask_restful import  Resource
from ..models.product_model import Product,products


class Products(Resource):
    """This class provides access to operations to GET and POST on products"""

    def get(self):
        """GETs all products"""
        return jsonify({"Products": products,
                        "status":200})

    def post(self):
        """Saves a new product item"""
        product_name = request.get_json("product_name")["product_name"].strip(" ")
        product_price = request.get_json("product_price")["product_price"]
        quantity = request.get_json("quantity")["quantity"]
        min_quantity = request.get_json("min_quantity")["min_quantity"]
        
        if not product_name or product_name=="" or not product_price :
            abort(400)

        if not request.json:
            abort(400)

        product = Product(product_name, product_price, quantity, min_quantity)
        newproduct = product.save_product()
        return jsonify({"Message":"Successfully saved",
                        "Product id saved": newproduct,
                        "status": 201})


class SingleProduct(Resource):
    """This resource will be used to retrieves a single product"""
    def get(self, product_id):
        """Gets a single product"""
        if not product_id or not isinstance(product_id, int):
            abort(404)		
        product = [product for product in products if product["product_id"] == product_id]
        if len(product) == 0:
            return jsonify({"Message": "No product found",
			    "status":404})
        return jsonify({"Product" : product,
            "status" : 200})