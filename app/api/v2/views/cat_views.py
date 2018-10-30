from flask import abort, jsonify, request
from flask_restful import  Resource
from flask_jwt_extended import jwt_required, get_jwt_claims
from db.db_config import open_connection, close_connection
from psycopg2 import Error
import psycopg2
from ..models.category_model import Category
from ..utils.decorators import admin_only, token_required

class Categories(Resource, Category):
    """Creates the endpoint for categories"""

    def __init__(self):
        """Initializes a category object"""
        self.category = Category()
    @jwt_required
    @admin_only
    def post(self):
        """Endpoint to add a new category"""
        cat_name = request.get_json("cat_name")["cat_name"].strip(" ")
        description = request.get_json("desc")["desc"].strip(" ")


        if not request.get_json:
            return jsonify({
                "message":"Data should be in json format",
                "status":400
            })
        
        return self.category.save_category(cat_name, description)    
        

class SingleCategory(Resource, Category):
    """Creates an endpoint for specific products"""

    def __init__(self):
        """Initializes a category object"""
        self.category = Category()
    @jwt_required
    @admin_only
    def put(self, cat_id):
        """Endpoint to delete a category"""
        cat_name = request.get_json("cat_name")["cat_name"].strip()
        cat_desc = request.get_json("desc")["desc"]

        
        return self.category.update_category(cat_id, cat_name, cat_desc)
            
    @jwt_required
    @admin_only
    def delete(self, cat_id):
        """Endpoint to delete a category"""
        
        return self.category.delete_category(cat_id)
