from flask import abort, jsonify, request
from flask_restful import  Resource
from ..models.product_model import Product
from flask_jwt_extended import jwt_required

# product = Product()
class Products(Resource, Product):
    """This class provides access to operations to GET and POST on products"""

    def __init___(self):
        pass


    @jwt_required
    def get(self):
        """GETs all products"""
        return jsonify({"Products": self.get_all_products(),
                        "status":200})
                        
    @jwt_required
    def post(self):
        """Saves a new product item"""
        product_name = request.get_json("product_name")["product_name"].strip(" ")
        product_price = request.get_json("product_price")["product_price"]
        quantity = request.get_json("quantity")["quantity"]
        min_quantity = request.get_json("min_quantity")["min_quantity"]
        
        if not product_name or product_name=="" or not product_price :
            return jsonify({"message":"You must provide product details",
                            "status":400})
        
        if not request.json:
            return jsonify({"message":"Input should be in json format",
                            "status":400})

        newproduct = self.save_product(product_name, product_price, quantity, min_quantity)
        return jsonify({"Message":"Successfully saved",
                        "Product id saved": newproduct,
                        "status": 201})


class SingleProduct(Resource, Product):
    """This resource will be used to retrieves a single product"""

    @jwt_required
    def get(self, product_id):
        """Gets a single product"""
        if not product_id or not isinstance(product_id, int):
            return jsonify({"message":"Please provide a valid product id(int)",
                            "status":404})		
        oneproduct = self.get_single_product(product_id)
        if len(oneproduct) == 0:
            return jsonify({"Product": "No product found",
			    "status":404})
        return jsonify({"Product" : oneproduct,
            "status" : 200})