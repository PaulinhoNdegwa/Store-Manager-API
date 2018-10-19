from flask import abort, jsonify, request, Blueprint
from flask_restful import  Resource, Api
from ..models.user_models import User,users
from flask_jwt_extended import jwt_required

class Users(Resource):
    """This class provides access to operations to GET and POST on users"""
    @jwt_required
    def get(self):
        """Gets all users"""
        return jsonify(users)
   

class SingleUser(Resource):
    """This resource will be used by the api to fetch specific sale"""
    @jwt_required
    def get(self, user_id):
        """Gets a single user"""
        if not user_id or not isinstance(user_id, int):
            abort(404)
        user  = [user for user in users if user_id == user["user_id"]]
        if len(user) == 0:
            return jsonify({"message":"User not found",
                            "status": 404})
        return jsonify({"User" : user,
                        "status" : 200})
