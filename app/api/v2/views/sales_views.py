from flask import abort, jsonify, request
from flask_restful import Resource
from ..models.sales_model import Sale
from ..models.user_models import User
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity
from ..utils.decorators import admin_only, atttendant_only, token_required
from flask_expects_json import expects_json
from ..utils.json_schemas import new_sale_schema

sale = Sale()
user = User()


class Sales(Resource):
    """This class provides access to operations to GET and POST on sales"""

    @jwt_required
    @admin_only
    def get(self):
        """Gets all sales orders"""

        return sale.get_all_sales()

    @jwt_required
    @atttendant_only
    @expects_json(new_sale_schema)
    def post(self):
        """Saves a new sales order"""
        data = request.get_json()
        product_name = data["product_name"].strip(" ")
        product_model = data["product_model"].strip(" ")
        quantity = data["quantity"]

        if not product_name or not product_model or not quantity:
            return jsonify({
                "message": "Product_name, product_model, quantity required",
                "status": 400
            })

        current_user = get_jwt_identity()["username"]

        return sale.save_sale(product_name, product_model,
                              quantity, current_user)


class SingleSale(Resource):
    """This resource will be used by the api to fetch specific sale"""

    @jwt_required
    @token_required
    def get(self, sale_id):
        """Gets a single sale order"""

        if not isinstance(sale_id, int) or not sale_id:
            return jsonify({"message": "Please provide a valid sale id(int)",
                            "status": 404})

        return sale.get_single_sale(sale_id)


class Profile(Resource):
    """This resource allows an attendant to fetch their details and sales"""
    @jwt_required
    @atttendant_only
    def get(self):
        """Attendant can view their information and sales made"""
        current_user = get_jwt_identity()["username"]

        personal_profile = user.get_user_by_username(current_user)
        profile = {
            "User id": personal_profile[0],
            "Email": personal_profile[1],
            "Role": personal_profile[2]
        }
        product_sales = user.get_user_product_sales(current_user)
        sales_list = []

        for product_sale in product_sales:

            sale = {
                "Product Id": product_sale[0],
                "Product Name": product_sale[1],
                "Product Model": product_sale[2],
                "Quantity sold": product_sale[3],
                "Total Price": product_sale[4]
            }
            sales_list.append(sale)

        return jsonify({
            "Message": "Successful",
            "Profile": profile,
            "Sales": sales_list,
            "status": 200
        })
