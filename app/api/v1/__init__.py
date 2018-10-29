from flask import Blueprint
from flask_restful import Api
from .views.product_views import Products, SingleProduct
from .views.sales_views import Sales, SingleSale
from .views.users_views import Users, SingleUser
from .views.auth_views import Register, Login

version_1 = Blueprint("api_v1", __name__, url_prefix='/api/v1')
api = Api(version_1)

auth_blueprint = Blueprint("api_auth_v1", __name__, url_prefix="/api/v1/auth")
auth_api_v1 = Api(auth_blueprint)

api.add_resource(Products, "/products")
api.add_resource(Sales, "/sales")
api.add_resource(Users, "/users")
api.add_resource(SingleProduct, "/products/<int:product_id>")
api.add_resource(SingleSale, "/sales/<int:sale_id>")
api.add_resource(SingleUser, "/users/<int:user_id>")


auth_api_v1.add_resource(Register, "/signup")
auth_api_v1.add_resource(Login, "/login")