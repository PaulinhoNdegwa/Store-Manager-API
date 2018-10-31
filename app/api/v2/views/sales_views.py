from flask import abort, jsonify, request
from flask_restful import  Resource
from ..models.sales_model import Sale
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity
from ..utils.decorators import *
from flask_expects_json import expects_json
from ..utils.json_schemas import new_sale_schema
    
class Sales(Resource, Sale):
    """This class provides access to operations to GET and POST on sales"""

    def __init__(self):
        self.sale = Sale()
        pass

    @jwt_required
    @admin_only
    def get(self):
        """Gets all sales orders"""
        
        return self.sale.get_all_sales()


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
                "message":"Product_name, product_model, quantity are required",
                "status": 400
            })
        
        current_user = get_jwt_identity()["username"]

        return self.sale.save_sale(product_name, product_model, quantity, current_user)
            

class SingleSale(Resource, Sale):
    """This resource will be used by the api to fetch specific sale"""

    def __init__(self):
        self.sale = Sale()


    @jwt_required
    @token_required
    def get(self, sale_id):
        """Gets a single sale order"""
        
        if not isinstance(sale_id, int) or not sale_id:
            return jsonify({"message":"Please provide a valid sale id(int)",
                            "status":404})
        
        return self.sale.get_single_sale(sale_id)
                            