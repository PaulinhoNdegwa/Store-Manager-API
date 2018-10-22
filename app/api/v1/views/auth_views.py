from flask import jsonify, request, json, Blueprint
from flask_restful import Api, Resource
from ..models.user_models import User, users
from flask_jwt_extended import create_access_token
import re

email_format = r"(^[a-zA-z0-9_.]+@[a-zA-z0-9-]+\.[a-z]+$)"

user = User()
class Register(Resource, User):

    def __init__(self):
        # self.user = User()
        pass

    def post(self):
        # data = request.get_json()
        email = request.get_json("email")["email"]
        password =request.get_json("password")["password"]
        role = request.get_json("role")["role"]       

        if not request.get_json:
            return jsonify("Data must be in json format")
        if not email or not password:
            return jsonify({"message":"You must provide username and password",
                            "status": 400})

        if not re.match(email_format, email):
            return jsonify({"message": "Please use a valid email format",
                            "status": 400})        

        user_exists = [user for user in users if email == user["email"]]

        if user_exists:
            return jsonify({"message":"User already exists"})

        else:
            user.save_user(email, password, role)
            return jsonify({
                "message":"User saved",
                "status": 201
            })
        
        

class Login(Resource, User):

    def post(self):
        # data = request.get_json()
        email = request.get_json("email")["email"]
        password =request.get_json("password")["password"]

        if not request.get_json:
            return jsonify("Data must be in json format")
        if not email or not password:
            return jsonify("You must provide username and password")
            
        if not re.match(email_format, email):
            return jsonify({"message": "Please use a valid email format",
                            "status": 400})  

        user_exists = [user for user in users if email == user["email"]]

        if not user_exists:
            return jsonify({
                "message":"User does not exist"
            })
        if password != user_exists[0]["password"]:
            return jsonify({
                "message":"Incorrect password",
                "status": 400
            })
        
        access_token = create_access_token(identity=email)
        return jsonify({
            "message":"Successfully logged in",
            "token": access_token,
            "status": 201
        })
        