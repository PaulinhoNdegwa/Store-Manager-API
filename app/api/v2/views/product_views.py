from flask import abort, jsonify, request
from flask_restful import Resource
from ..models.product_model import Product
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity
from ..utils.decorators import admin_only, atttendant_only, token_required
from flask_expects_json import expects_json
from ..utils.json_schemas import product_schema

product = Product()


class Products(Resource, Product):
    """This class provides access to operations to GET and POST on products"""

    @jwt_required
    @token_required
    def get(self):
        """GETs all products"""
        return jsonify({"Products": self.get_all_products(),
                        "status": 200})

    @jwt_required
    @admin_only
    @expects_json(product_schema)
    def post(self):
        """Saves a new product item"""
        data = request.get_json()
        product_name = data["product_name"].strip(" ")
        model = data["model"].strip(" ")
        category = data["category"].strip(" ")
        product_price = data["product_price"]
        quantity = data["quantity"]
        min_quantity = data["min_quantity"]

        if not product_name or not model or not product_price or not quantity \
                or not min_quantity:
            return jsonify({
                "message": "All fields are required",
                "status": 400
            })

        current_user = get_jwt_identity()["username"].lower()

        product = {
            "product_name": product_name,
            "model": model,
            "category": category,
            "product_price": product_price,
            "quantity": quantity,
            "min_quantity": min_quantity,
            "created_by": current_user
        }

        return Product().save_product(**product)


class SingleProduct(Resource, Product):
    """This resource will be used to retrieves a single product"""

    def __init__(self):
        pass

    @jwt_required
    @token_required
    def get(self, product_id):
        """Gets a single product"""

        return product.get_single_product(product_id)

    @jwt_required
    @admin_only
    @expects_json(product_schema)
    def put(self, product_id):
        """Endpoint to update a product"""

        product_name = request.get_json("product_name")[
            "product_name"].strip(" ")
        model = request.get_json("model")["model"].strip(" ")
        product_price = request.get_json("product_price")["product_price"]
        quantity = request.get_json("quantity")["quantity"]
        category = request.get_json("category")[("category")]
        min_quantity = request.get_json("min_quantity")["min_quantity"]

        if not product_name or not model or not product_price or not quantity \
                or not min_quantity:
            return jsonify({
                "message": "Check all required fields",
                "status": 400
            })

        current_user = get_jwt_identity()["username"].lower()

        product = {
            "product_id": product_id,
            "product_name": product_name,
            "model": model,
            "product_price": product_price,
            "quantity": quantity,
            "category": category,
            "min_quantity": min_quantity,
            "created_by": current_user
        }

        return Product().update_product(**product)

    @jwt_required
    @admin_only
    def delete(self, product_id):
        """End point to delete product"""

        return product.delete_product(product_id)
