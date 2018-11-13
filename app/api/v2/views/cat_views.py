from flask import abort, jsonify, request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_claims
from db.db_config import open_connection, close_connection
from psycopg2 import Error
import psycopg2
from ..models.category_model import Category
from ..utils.decorators import admin_only, token_required
from flask_expects_json import expects_json
from ..utils.json_schemas import category_schema

category = Category()


class Categories(Resource):
    """Creates the endpoint for categories"""
    @jwt_required
    @admin_only
    def get(self):
        """Endpoint to get all categories"""

        return category.get_all_categories()
        

    @jwt_required
    @admin_only
    @expects_json(category_schema)
    def post(self):
        """Endpoint to add a new category"""
        cat_name = request.get_json("cat_name")["cat_name"].strip(" ")
        description = request.get_json("desc")["desc"].strip(" ")

        if not cat_name or not description:
            return jsonify({
                "message": "Category name and description are required",
                "status": 400
            })

        return category.save_category(cat_name, description)


class SingleCategory(Resource):
    """Creates an endpoint for specific products"""

    @jwt_required
    @admin_only
    @expects_json(category_schema)
    def put(self, cat_id):
        """Endpoint to delete a category"""
        cat_name = request.get_json("cat_name")["cat_name"].strip(" ")
        cat_desc = request.get_json("desc")["desc"].strip(" ")

        if not cat_name or not cat_desc:
            return jsonify({
                "message": "Category name and description are required",
                "status": 400
            })

        return category.update_category(cat_id, cat_name, cat_desc)

    @jwt_required
    @admin_only
    def delete(self, cat_id):
        """Endpoint to delete a category"""

        return category.delete_category(cat_id)
