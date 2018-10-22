from flask import abort, jsonify, request
from flask_restful import  Resource
from ..models.user_models import User,users


class Users(Resource):
    """This class provides access to operations to GET and POST on users"""

    def get(self):
        """Gets all users"""
        return jsonify(users)

    def post(self):
        """Saves a new user"""
        f_name = request.get_json("f_name")["f_name"].strip(" ")
        s_name = request.get_json("s_name")["s_name"].strip(" ")
        email = request.get_json("email")["email"].strip(" ")
        password = request.get_json("password")["password"].strip(" ")
        role = request.get_json("role")["role"].strip(" ")

        user = User(f_name,s_name,email, password, role)
        newuser = user.save_user()
        return jsonify({"Message":"Successfully saved",
                        "User saved": newuser,
                        "status": 201})




class SingleUser(Resource):
    """This resource will be used by the api to fetch specific sale"""

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
