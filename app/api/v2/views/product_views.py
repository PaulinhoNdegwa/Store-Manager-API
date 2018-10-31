from flask import abort, jsonify, request
from flask_restful import Resource
from ..models.product_model import Product
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity
from ..utils.decorators import admin_only, atttendant_only, token_required
from flask_expects_json import expects_json
from ..utils.json_schemas import new_product_schema, update_product_schema


class Products(Resource, Product):
    """This class provides access to operations to GET and POST on products"""

    def __init___(self):
        pass


    @jwt_required
    @atttendant_only
    def get(self):
        """GETs all products"""
        return jsonify({"Products": self.get_all_products(),
                        "status":200})
                        
    @jwt_required
    @admin_only
    @expects_json(new_product_schema)
    def post(self):
        """Saves a new product item"""
        product_name = request.get_json("product_name")["product_name"].strip(" ")
        model = request.get_json("model")["model"].strip(" ")
        product_price = request.get_json("product_price")["product_price"]
        quantity = request.get_json("quantity")["quantity"]
        min_quantity = request.get_json("min_quantity")["min_quantity"]

        current_user = get_jwt_identity()["username"].lower()
       
        product= {
            "product_name": product_name,
            "model": model,
            "product_price":product_price,
            "quantity":quantity,
            "min_quantity": min_quantity,
            "created_by": current_user
        }
        
        return self.save_product(**product)
        


class SingleProduct(Resource, Product):
    """This resource will be used to retrieves a single product"""

    def __init__(self):
        pass

    @jwt_required
    @token_required
    def get(self, product_id):
        """Gets a single product"""
        		        
        return self.get_single_product(product_id)

    @jwt_required
    @admin_only
    @expects_json(update_product_schema)
    def put(self, product_id):
        """Endpoint to update a product"""

        product_name = request.get_json("product_name")["product_name"].strip(" ")
        model = request.get_json("model")["model"].strip(" ")
        product_price = request.get_json("product_price")["product_price"]
        quantity = request.get_json("quantity")["quantity"]
        min_quantity = request.get_json("min_quantity")["min_quantity"]

        current_user = get_jwt_identity()["username"].lower()
        print(current_user)
        
        product= {
            "product_id": product_id,
            "product_name": product_name,
            "model": model,
            "product_price":product_price,
            "quantity":quantity,
            "min_quantity": min_quantity,
            "created_by": current_user
        }
        
        
        return self.update_product(**product)

    @jwt_required
    @admin_only
    def delete(self, product_id):
        """End point to delete product"""
        
        return self.delete_product(product_id)
        