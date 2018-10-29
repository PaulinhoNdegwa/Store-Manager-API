from flask import jsonify, request, json
from flask_restful import Resource
from ..models.user_models import User
from flask_jwt_extended import jwt_required, get_jwt_claims, JWTManager,get_jwt_identity, get_raw_jwt


class Register(Resource, User):

    def __init__(self):
        self.user = User()

    @jwt_required
    def post(self):
        # data = request.get_json()
        email = request.get_json("email")["email"]
        password =request.get_json("password")["password"]
        confirm_password =request.get_json("confirm_password")["confirm_password"]
        role = request.get_json("role")["role"]

        user = get_jwt_identity()["username"].lower()
        print(user)

        role_claim=get_jwt_claims()["role"].lower()
        if role_claim !="admin":
            print("not admin")
            return jsonify({
                "message":"Unauthorized! You are not an admin",
                "status":401
            })
        # print("admin")
        
        return self.user.save_user(email, password, confirm_password, role)
            


class Login(Resource, User):
    """Log in endpoint"""

    def __init__(self):

        self.user = User()

    def post(self):
        # data = request.get_json()
        email = request.get_json("email")["email"]
        password =request.get_json("password")["password"]

        return self.user.user_login(email, password)


class Logout(Resource, User):
    """End point to log out a user"""

    def __init__(self):
        self.user = User()

    @jwt_required
    def delete(self):
        if "Authorization" in request.headers:            
            token = request.headers["Authorization"]
            
            return self.user.blacklist_token(str(token))