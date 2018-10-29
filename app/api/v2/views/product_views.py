from flask import abort, jsonify, request
from flask_restful import  Resource
from ..models.product_model import Product
from flask_jwt_extended import jwt_required, get_jwt_claims

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
        model = request.get_json("model")["model"].strip(" ")
        product_price = request.get_json("product_price")["product_price"]
        quantity = request.get_json("quantity")["quantity"]
        min_quantity = request.get_json("min_quantity")["min_quantity"]

        role_claim=get_jwt_claims()["role"].lower()
        print(role_claim)
        if role_claim !="admin":
            # print("not admin")
            return jsonify({
                "message":"Unauthorized! You are not an admin",
                "status":403
            })
        
        
        return self.save_product(product_name, model, product_price, quantity, min_quantity)
        


class SingleProduct(Resource, Product):
    """This resource will be used to retrieves a single product"""

    def __init__(self):
        pass

    @jwt_required
    def get(self, product_id):
        """Gets a single product"""
        		        
        return self.get_single_product(product_id)

    @jwt_required
    def put(self, product_id):
        """Endpoint to update a product"""

        product_name = request.get_json("product_name")["product_name"].strip(" ")
        model = request.get_json("model")["model"].strip(" ")
        product_price = request.get_json("product_price")["product_price"]
        quantity = request.get_json("quantity")["quantity"]
        min_quantity = request.get_json("min_quantity")["min_quantity"]

        role_claim=get_jwt_claims()["role"].lower()
        print(role_claim)
        if role_claim !="admin":
            # print("not admin")
            return jsonify({
                "message":"Unauthorized! You are not an admin",
                "status":403
            })
        
        
        return self.update_product(product_id,product_name, model, product_price, quantity, min_quantity)

    @jwt_required
    def delete(self, product_id):
        """End point to delete product"""
        role_claim=get_jwt_claims()["role"].lower()
        print(role_claim)
        if role_claim !="admin":
            # print("not admin")
            return jsonify({
                "message":"Unauthorized! You are not an admin",
                "status":403
            })

        return self.delete_product(product_id)
        