from flask import Flask
from flask_restful import Api

from Instance.config import app_config
from flask_jwt_extended import JWTManager 

def create_app(config_name):

    storemanager = Flask(__name__, instance_relative_config=True)
    storemanager.config["JWT_SECRET_KEY"] = "mysecretkey"
    jwt = JWTManager(storemanager)

    storemanager.url_map.strict_slashes = False
    storemanager.config.from_object(app_config[config_name])
    # storemanager.config["TESTING"] = True

    from .api.v1 import app_blueprint as v1
    storemanager.register_blueprint(v1)

    from .api.v1 import auth_blueprint as auth_bp
    storemanager.register_blueprint(auth_bp)

    return storemanager