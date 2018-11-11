from flask import Flask
from flask_restful import Api

from Instance.config import app_config
from settings import load_env_var
from db import tables
from flask_jwt_extended import JWTManager
from app.api.v2.utils.error_handlers import *
from flask_cors import CORS


def create_app(config_name):
    """This function returns an instance of the API"""
    load_env_var()
    storemanager = Flask(__name__, instance_relative_config=True)
    storemanager.config["JWT_SECRET_KEY"] = "mysecretkey"
    jwt = JWTManager(storemanager)
    CORS(storemanager)

    storemanager.url_map.strict_slashes = False
    storemanager.config.from_object(app_config[config_name])

    from .api.v1 import version_1 as v1
    storemanager.register_blueprint(v1)

    from .api.v1 import auth_blueprint as auth_bp
    storemanager.register_blueprint(auth_bp)

    from .api.v2 import version_2 as v2
    storemanager.register_blueprint(v2)

    from .api.v2 import auth_blueprint_v2 as auth_bp_v2
    storemanager.register_blueprint(auth_bp_v2)

    # Add app error handlers
    storemanager.register_error_handler(404, resource_not_found)
    storemanager.register_error_handler(405, method_not_allowed)
    storemanager.register_error_handler(401, missing_auth_header)

    @storemanager.errorhandler(Exception)
    def unhandled_exception(e):
        return jsonify({"message": "Server error. Contact the admin",
                        "status": 500})

    @jwt.user_claims_loader
    def add_claim_to_access_token(user_identity):
        return {"role": user_identity["role"]}

    @jwt.user_identity_loader
    def user_identity_lookup(user_identity):
        return {"username": user_identity["username"]}

    return storemanager
