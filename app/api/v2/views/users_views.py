from flask import abort, jsonify, request, Blueprint
from flask_restful import Resource
from ..models.user_models import User
from flask_jwt_extended import jwt_required, get_jwt_claims, get_jwt_identity
from ..utils.decorators import admin_only, atttendant_only, token_required
from flask_expects_json import expects_json
from ..utils.json_schemas import update_role_schema


class Users(Resource, User):
    """This class provides access to operations to GET and POST on users"""

    def __init__(self):
        pass

    @jwt_required
    @admin_only
    def get(self):
        """Gets all users"""

        return self.get_all_users()


class SingleUser(Resource, User):
    """This resource will be used by the api to fetch specific sale"""

    def __init__(self):
        self.user = User()

    @jwt_required
    @token_required
    def get(self, user_id):
        """Gets a single user"""
        user = get_jwt_identity()["username"].lower()

        user_exists = self.user.get_user_by_id(user_id)

        if not user_exists:
            return jsonify({"message": "User not found",
                            "status": 404})
        user = {
            "User Id": user_exists[0],
            "Email": user_exists[1],
            "Role": user_exists[3]
        }
        return jsonify({
            "Message": "Successful",
            "User": user,
            "status": 200
        })

    @jwt_required
    @admin_only
    @expects_json(update_role_schema)
    def put(self, user_id):
        """Allows admin to set Attendant as admin"""

        role = request.get_json("role")["role"].strip(" ")

        if not user_id or not isinstance(user_id, int):
            return jsonify({"message": "Please provide a valid user id(int)",
                            "status": 404})

        return self.user.update_role(user_id, role)
