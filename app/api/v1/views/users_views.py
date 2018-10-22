from flask import abort, jsonify, request, Blueprint
from flask_restful import  Resource
from ..models.user_models import User
from flask_jwt_extended import jwt_required

class Users(Resource, User):
    """This class provides access to operations to GET and POST on users"""

    def __init__(self):
        pass


    @jwt_required
    def get(self):
        """Gets all users"""
        return jsonify(self.get_all_users())
   

class SingleUser(Resource, User):
    """This resource will be used by the api to fetch specific sale"""
    @jwt_required
    def get(self, user_id):
        """Gets a single user"""
        if not user_id or not isinstance(user_id, int):
            return jsonify({"message":"Please provide a valid user id(int)",
                            "status":404})
        user = self.get_user(user_id)
        if len(user) == 0:
            return jsonify({"message":"User not found",
                            "status": 404})
        return jsonify({"User" : user,
                        "status" : 200})
