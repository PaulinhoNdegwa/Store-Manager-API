from flask import Blueprint
from flask_restful import Api

version_2 = Blueprint("api_v2", __name__, url_prefix="api/v2")
api = Api(version_2)