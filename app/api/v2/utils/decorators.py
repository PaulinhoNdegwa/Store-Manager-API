from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import get_jwt_claims
from app.api.v2.models.user_models import User


def token_required(f):
    """This decorator checks the presence of token on protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        """This methoD checks for the presence of a token in
        the Authorization header"""
        token = None
        if "Authorization" in request.headers:
            token = str(request.headers["Authorization"][7:-1])
        if not token:
            return ({
                "Message": "Unsuccessful, token is required. Log in",
                "Status": 401
            })
        user_object = User()
        token_blacklisted = user_object.lookup_token(token)
        if token_blacklisted:
            return ({
                "Message": "Unsuccessful, token is invalid. Log in again",
                "Status": 401
            })
        return f(*args, **kwargs)
    return decorated


def admin_only(f):
    """This decorator checks the presence of an admin token on admin routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        """This decorator protects admin only routes"""

        token = None
        if "Authorization" in request.headers:
            token = str(request.headers["Authorization"][7:-1])
        if not token:
            return ({
                "Message": "Unsuccessful, token is required. Log in",
                "Status": 401
            })
        user_object = User()
        token_blacklisted = user_object.lookup_token(token)
        if token_blacklisted is True:
            return ({
                "Message": "Unsuccessful, token is invalid. Log in again",
                "Status": 401
            })

        role_claim = get_jwt_claims()["role"].lower()
        if role_claim != "admin":
            print("not admin")
            return jsonify({
                "message": "Unauthorized! You are not an admin",
                "status": 401
            })
        return f(*args, **kwargs)
    return decorated


def atttendant_only(f):
    """This decorator checks the presence of an attendant token"""
    @wraps(f)
    def decorated(*args, **kwargs):
        """This decorator protects attendant only routes"""

        token = None
        if "Authorization" in request.headers:
            token = str(request.headers["Authorization"][7:-1])
        if not token:
            return ({
                "Message": "Unsuccessful, token is required. Log in",
                "Status": 401
            })
        user_object = User()
        token_blacklisted = user_object.lookup_token(token)
        if token_blacklisted is True:
            return ({
                "Message": "Unsuccessful, token is invalid. Log in again",
                "Status": 401
            })
        role_claim = get_jwt_claims()["role"].lower()
        print(role_claim)
        if role_claim != "attendant":
            print("not attendant")
            return jsonify({
                "message": "Unauthorized! You are not an attendant",
                "status": 401
            })
        return f(*args, **kwargs)
    return decorated
