from flask import abort, jsonify, request, Blueprint
from flask_restful import  Resource
from ..models.user_models import User
from flask_jwt_extended import jwt_required, get_jwt_claims


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
    def __init__(self):
        self.user = User()
        
    @jwt_required
    def get(self, user_id):
        """Gets a single user"""
        if not user_id or not isinstance(user_id, int):
            return jsonify({"message":"Please provide a valid user id(int)",
                            "status":404})
        user_exists =  self.user.get_user_by_id(user_id)

        if not user_exists:
            return jsonify({"message":"User not found",
                            "status": 404})
        return jsonify({"User" : user_exists,
                        "status" : 200})

    @jwt_required
    def put(self, user_id):
        """Allows admin to set Attendant as admin"""

        role_claim=get_jwt_claims()["role"].lower()
        if role_claim !="admin":
            print("not admin")
            return jsonify({
                "message":"Unauthorized! You are not an admin",
                "status":400
            })
        if not user_id or not isinstance(user_id, int):
            return jsonify({"message":"Please provide a valid user id(int)",
                            "status":404})
        
        return self.user.set_admin(user_id)