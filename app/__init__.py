from flask import Flask
from flask_restful import Api

from Instance.config import app_config
from settings import load_env_var
from db import tables
from flask_jwt_extended import JWTManager 

def create_app(config_name):
	"""This function returns an instance of the API"""
	load_env_var()	
	storemanager = Flask(__name__, instance_relative_config=True)
	storemanager.config["JWT_SECRET_KEY"] = "mysecretkey"
	jwt = JWTManager(storemanager)

	storemanager.url_map.strict_slashes = False
	storemanager.config.from_object(app_config[config_name])
	# storemanager.config["TESTING"] = True

	from .api.v1 import version_1 as v1
	storemanager.register_blueprint(v1)

	from .api.v1 import auth_blueprint as auth_bp
	storemanager.register_blueprint(auth_bp)

	from .api.v2 import version_2 as v2
	storemanager.register_blueprint(v2)   

	from .api.v2 import auth_blueprint_v2 as auth_bp_v2
	storemanager.register_blueprint(auth_bp_v2) 
	# tables.create_tables()

		
	@jwt.user_claims_loader
	def add_claim_to_access_token(role):
		return {"role":role}

	return storemanager

	
