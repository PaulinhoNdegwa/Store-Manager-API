from flask import jsonify, request, json
from flask_restful import Resource
from ..models.user_models import User
from flask_jwt_extended import (jwt_required, get_jwt_claims, JWTManager,
                                get_jwt_identity, get_raw_jwt)
from ..utils.decorators import admin_only, atttendant_only, token_required
from flask_expects_json import expects_json
from ..utils.json_schemas import register_schema, login_schema

user = User()


class Register(Resource):

    # def __init__(self):
    #     self.user = User()

    @jwt_required
    @admin_only
    @expects_json(register_schema)
    def post(self):
        data = request.get_json()
        email = data["email"]
        password = data["password"]
        confirm_password = data["confirm_password"]
        role = data["role"]

        if not email or not password or not confirm_password or not role:
            return jsonify({
                "message": "All fields are required",
                "status": 400
            })

        return user.save_user(email, password, confirm_password, role)


class Login(Resource):

    @expects_json(login_schema)
    def post(self):
        data = request.get_json()
        email = data["email"]
        password = data["password"]

        if not email or not password:
            return jsonify({
                "message": "Email and password are required",
                "status": 400
            })

        return user.user_login(email, password)


class Logout(Resource):
    """End point to log out a user"""

    @jwt_required
    @token_required
    def put(self):
        if "Authorization" in request.headers:
            token = request.headers["Authorization"]

            return user.blacklist_token(str(token))
