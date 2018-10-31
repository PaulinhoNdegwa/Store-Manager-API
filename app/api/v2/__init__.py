from flask import Blueprint
from flask_restful import Api
from .views.product_views import Products, SingleProduct
from .views.sales_views import Sales, SingleSale
from .views.users_views import Users, SingleUser
from .views.auth_views import Register, Login, Logout
from .views.cat_views import Categories, SingleCategory

version_2 = Blueprint("api_v2", __name__, url_prefix="/api/v2")
api_v2 = Api(version_2)

auth_blueprint_v2 = Blueprint("api_auth_v2", __name__,
                              url_prefix="/api/v2/auth")
auth_api_v2 = Api(auth_blueprint_v2)

api_v2.add_resource(Products, "/products")
api_v2.add_resource(Sales, "/sales")
api_v2.add_resource(Users, "/users")
api_v2.add_resource(SingleProduct, "/products/<int:product_id>")
api_v2.add_resource(SingleSale, "/sales/<int:sale_id>")
api_v2.add_resource(SingleUser, "/users/<int:user_id>")

api_v2.add_resource(Categories, "/category")
api_v2.add_resource(SingleCategory, "/category/<int:cat_id>")

auth_api_v2.add_resource(Register, "/signup")
auth_api_v2.add_resource(Login, "/login")
auth_api_v2.add_resource(Logout, "/logout")
