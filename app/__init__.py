from flask import Flask
from flask_restful import Api

from Instance.config import app_config

def create_app(config_name):

    storemanager = Flask(__name__, instance_relative_config=True)

    storemanager.url_map.strict_slashes = False
    storemanager.config.from_object(app_config[config_name])
    # storemanager.config["TESTING"] = True

    from .api.v1 import app_blueprint as v1
    storemanager.register_blueprint(v1)

    return storemanager