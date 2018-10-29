from flask import abort, jsonify, request
from flask_restful import  Resource
from ..models.sales_model import Sale
from flask_jwt_extended import jwt_required, get_jwt_claims
    
class Sales(Resource, Sale):
    """This class provides access to operations to GET and POST on sales"""

    def __init__(self):
        self.sale = Sale()
        pass

    @jwt_required
    def get(self):
        """Gets all sales orders"""
        role_claim=get_jwt_claims()["role"].lower()
        # print(role_claim)
        if role_claim !="admin":
            return jsonify({
                "message":"Unauthorized! You are not an admin",
                "status":401
            })

        return self.sale.get_all_sales()

    @jwt_required
    def post(self):
        """Saves a new sales order"""
        
        product_name = request.get_json("product_name")["product_name"].strip(" ")
        product_model = request.get_json("product_model")["product_model"]
        quantity = request.get_json("quantity")["quantity"]

        return self.sale.save_sale(product_name, product_model, quantity)
        

class SingleSale(Resource, Sale):
    """This resource will be used by the api to fetch specific sale"""

    def __init__(self):
        self.sale = Sale()


    @jwt_required
    def get(self, sale_id):
        """Gets a single sale order"""
        role_claim=get_jwt_claims()["role"].lower()
        print(role_claim)
        if role_claim !="admin":
            return jsonify({
                "message":"Unauthorized! You are not an admin",
                "status":401
            })
        if not isinstance(sale_id, int) or not sale_id:
            return jsonify({"message":"Please provide a valid sale id(int)",
                            "status":404})
        
        return self.sale.get_single_sale(sale_id)
                            